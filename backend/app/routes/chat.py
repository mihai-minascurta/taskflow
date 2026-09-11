"""
Chat endpoint backing the in-app assistant widget.

Uses the official OpenAI Python SDK pointed at Groq's OpenAI-compatible
base URL, with the project's remote MCP server (taskflow_infra) attached
as a tool. Groq handles tool discovery and the call/execute loop against
that server on its own — this endpoint just forwards the user's message
and relays the final answer back to the frontend. No chat history is
persisted server-side; the frontend keeps the `response_id` and sends it
back to continue a conversation (Groq's `previous_response_id`).

Required environment variables (see .env.example):
    GROQ_API_KEY     - API key from https://console.groq.com
    MCP_SERVER_URL   - public HTTPS URL of the remote MCP server,
                        including its path (e.g. https://mcp.example.com/mcp)

Optional:
    GROQ_MODEL              - defaults to "openai/gpt-oss-20b"
    MCP_SERVER_LABEL        - defaults to "taskflow_infra"
    MCP_SERVER_DESCRIPTION  - shown to the model; defaults to a generic description
"""

import logging

from flask import Blueprint, current_app, g, jsonify, request
from openai import OpenAI, OpenAIError

from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__)


def _extract_reply_text(response) -> str:
    """Pull the assistant's final text out of a Responses API result,
    ignoring the model's internal reasoning.

    Tries the SDK's `output_text` convenience property first (it already
    only reads "message" items), but falls back to walking `output`
    manually — some SDK versions raise when a content item's text is
    null instead of an empty string (see openai-python#3011 / #2822).
    The fallback filters to "message" items with "output_text" content,
    same as the convenience property does — an unfiltered walk would
    otherwise also pick up "reasoning" items (gpt-oss models think out
    loud before answering) and leak that chain-of-thought into the reply.
    """
    try:
        text = response.output_text
        if text:
            return text
    except Exception:  # defensive: see openai-python#3011
        pass

    chunks = []
    for item in getattr(response, "output", None) or []:
        if getattr(item, "type", None) != "message":
            continue
        for part in getattr(item, "content", None) or []:
            if getattr(part, "type", None) != "output_text":
                continue
            text = getattr(part, "text", None)
            if text:
                chunks.append(text)
    return "\n".join(chunks).strip()


@chat_bp.route("/chat", methods=["POST"])
@login_required
def send_chat_message():
    api_key = current_app.config.get("GROQ_API_KEY")
    mcp_url = current_app.config.get("MCP_SERVER_URL")
    if not api_key or not mcp_url:
        raise APIError(
            "Chat assistant is not configured (missing GROQ_API_KEY / MCP_SERVER_URL)",
            503,
        )

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        raise APIError("'message' is required", 400)

    previous_response_id = data.get("previous_response_id")

    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    kwargs = {
        "model": current_app.config.get("GROQ_MODEL", "openai/gpt-oss-20b"),
        "input": message,
        "instructions": (
            "You are the TaskFlow infrastructure assistant. Answer directly "
            "and concisely, in the same language as the user's question. "
            "Never show your internal reasoning — only the final answer."
        ),
        "tools": [
            {
                "type": "mcp",
                "server_label": current_app.config.get(
                    "MCP_SERVER_LABEL", "taskflow_infra"
                ),
                "server_description": current_app.config.get(
                    "MCP_SERVER_DESCRIPTION",
                    "Kubernetes and AWS infrastructure tools for the TaskFlow environment.",
                ),
                "server_url": mcp_url,
                "require_approval": "never",
            }
        ],
    }
    if previous_response_id:
        kwargs["previous_response_id"] = previous_response_id

    try:
        response = client.responses.create(**kwargs)
    except OpenAIError as exc:
        logger.error("Groq API request failed: %s", exc)
        raise APIError("Chat assistant is temporarily unavailable", 502)

    reply = (
        _extract_reply_text(response)
        or "Sorry, I didn't get a usable answer that time."
    )

    logger.info("Chat message handled for user %s", g.current_user.username)
    return jsonify({"reply": reply, "response_id": response.id}), 200
