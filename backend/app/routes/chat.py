
"""
Chat endpoint backing the in-app assistant widget.

Uses the official OpenAI Python SDK pointed at Groq's OpenAI-compatible
base URL, with the project's remote MCP server (taskflow_infra) attached
as a tool.

Groq's Responses API does not support previous_response_id, so the
frontend sends the conversation history with every request.
"""

import logging

from flask import Blueprint, current_app, g, jsonify, request
from openai import OpenAI, OpenAIError

from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__)


def _extract_reply_text(response) -> str:
    """Pull the assistant's final text out of a Responses API result."""

    try:
        text = response.output_text
        if text:
            return text
    except Exception:
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

    # Frontend keeps the conversation history.
    messages = data.get("messages") or []

    if not isinstance(messages, list):
        raise APIError("'messages' must be an array", 400)

    # Basic validation: only accept user/assistant text messages.
    conversation = []

    for item in messages:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        text = item.get("text")

        if role not in ("user", "assistant"):
            continue

        if not isinstance(text, str) or not text.strip():
            continue

        conversation.append(
            {
                "role": role,
                "content": text.strip(),
            }
        )

    # Add the current user message.
    conversation.append(
        {
            "role": "user",
            "content": message,
        }
    )

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    kwargs = {
        "model": current_app.config.get(
            "GROQ_MODEL",
            "openai/gpt-oss-20b",
        ),
        "input": conversation,
        "instructions": (
            "You are the TaskFlow infrastructure assistant. "
            "Answer directly and concisely, in the same language as "
            "the user's question. "
            "Use the available MCP tools when the question requires "
            "current information about the TaskFlow AWS/Kubernetes "
            "infrastructure. "
            "Never show your internal reasoning — only the final answer."
        ),
        "tools": [
            {
                "type": "mcp",
                "server_label": current_app.config.get(
                    "MCP_SERVER_LABEL",
                    "taskflow_infra",
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

    try:
        response = client.responses.create(**kwargs)

    except OpenAIError as exc:
        logger.error("Groq API request failed: %s", exc)

        raise APIError(
            "Chat assistant is temporarily unavailable",
            502,
        )

    reply = (
        _extract_reply_text(response)
        or "Sorry, I didn't get a usable answer that time."
    )

    logger.info(
        "Chat message handled for user %s",
        g.current_user.username,
    )

    return jsonify(
        {
            "reply": reply,
        }
    ), 200
