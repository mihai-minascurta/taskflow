"""
Centralized error handling.

Routes raise `APIError` for expected/handled failures (bad input, not found,
unauthorized, etc.) so the response format stays consistent everywhere:

    { "error": "<message>" }

Unexpected exceptions are caught by the generic handler, logged with a full
stack trace, and returned to the client as a generic 500 without leaking
internal details.
"""

import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Raised deliberately by route handlers for expected error conditions."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def register_error_handlers(app) -> None:
    @app.errorhandler(APIError)
    def handle_api_error(error: APIError):
        logger.warning("API error (%s): %s", error.status_code, error.message)
        return jsonify({"error": error.message}), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):
        logger.warning("HTTP exception (%s): %s", error.code, error.description)
        return jsonify({"error": error.description}), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        logger.exception("Unhandled exception: %s", error)
        return jsonify({"error": "Internal server error"}), 500
