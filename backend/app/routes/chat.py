"""
Chat endpoint backing the in-app assistant widget.

Wraps Groq's Responses API (OpenAI-compatible) and hands it the project's
remote MCP server as a tool, so Groq handles tool discovery and the
call/execute loop against that server on its own. This endpoint just
forwards the user's message and relays the final answer back to the
frontend — no chat history is persisted server-side; the frontend keeps
the `response_id` around and sends it back to continue the conversation
(see Groq's `previous_response_id`).

Required environment variables (see .env.example):
    GROQ_API_KEY     - API key from https://console.groq.com
    MCP_SERVER_URL   - public HTTPS URL of the remote MCP server (ALB)

Optional:
    GROQ_MODEL        - defaults to "openai/gpt-oss-120b"
    MCP_SERVER_LABEL  - defaults to "taskflow-mcp"
"""

import logging

import requests
from flask import Blueprint, current_app, g, jsonify, request

from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

chat_bp = Blueprint("chat", __name__)

GROQ_RESPONSES_URL = "https://api.groq.com/openai/v1/responses"


def _extract_reply_text(payload: dict) -> str:
    """Pull the assistant's text out of a Responses API payload.

    Parsed defensively (rather than assuming one fixed shape) since this
    is a third-party API response.
    """
    output_text = payload.get("output_text")
    if isinstance(output_text, str) and output_text:
        return output_text

    chunks = []
    for item in payload.get("output", []) or []:
        for part in item.get("content", []) or []:
            text = part.get("text")
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

    body = {
        "model": current_app.config.get("GROQ_MODEL", "openai/gpt-oss-120b"),
        "input": message,
        "tools": [
            {
                "type": "mcp",
                "server_label": current_app.config.get("MCP_SERVER_LABEL", "taskflow-mcp"),
                "server_url": mcp_url,
                "require_approval": "never",
            }
        ],
    }
    if previous_response_id:
        body["previous_response_id"] = previous_response_id

    try:
        response = requests.post(
            GROQ_RESPONSES_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=body,
            timeout=30,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("Groq API request failed: %s", exc)
        raise APIError("Chat assistant is temporarily unavailable", 502)

    payload = response.json()
    reply = _extract_reply_text(payload) or "Sorry, I didn't get a usable answer that time."

    logger.info("Chat message handled for user %s", g.current_user.username)
    return (
        jsonify(
            {
                "reply": reply,
                "response_id": payload.get("id"),
            }
        ),
        200,
    )
