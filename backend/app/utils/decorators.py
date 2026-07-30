"""
Very small "fake auth" helper.

This project does not use a real authentication framework (JWT, sessions,
OAuth, etc.) per project scope — see app/routes/auth.py for how the token is
issued. This decorator just checks that *some* token issued by our own login
endpoint is present and resolves it back to a user, so protected endpoints at
least require having "logged in" first.

# TODO: replace this whole mechanism with a real auth solution
# (e.g. Flask-Login + hashed sessions, or JWT with expiry/refresh) before
# this application handles anything sensitive.
"""

import base64
import binascii
import logging
from functools import wraps

from flask import g, request

from app.models.user import User
from app.utils.errors import APIError

logger = logging.getLogger(__name__)


def decode_fake_token(token: str):
    try:
        decoded = base64.b64decode(token).decode("utf-8")
        user_id_str, username, _issued_at = decoded.split(":", 2)
        return int(user_id_str), username
    except (ValueError, binascii.Error, UnicodeDecodeError):
        return None, None


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise APIError("Missing or invalid Authorization header", 401)

        token = auth_header.removeprefix("Bearer ").strip()
        user_id, _username = decode_fake_token(token)
        if user_id is None:
            raise APIError("Invalid token", 401)

        user = User.query.get(user_id)
        if user is None:
            raise APIError("User for token no longer exists", 401)

        g.current_user = user
        return view_func(*args, **kwargs)

    return wrapped
