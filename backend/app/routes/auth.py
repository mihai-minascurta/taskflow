"""
Authentication routes.

# TODO: This is a deliberately simplified "fake login" for this version of
# the app (per project scope, no real auth framework is required). The
# "token" is just a base64-encoded string, it never expires, and it is not
# signed/verified against SECRET_KEY. Do not reuse this pattern in a real
# production system — swap in real sessions or JWTs (with expiry + refresh)
# before this app handles anything sensitive.
"""

import base64
import logging
from datetime import datetime, timezone

from flask import Blueprint, g, jsonify, request

from app.models.user import User
from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)


def _issue_fake_token(user: User) -> str:
    raw = f"{user.id}:{user.username}:{datetime.now(timezone.utc).isoformat()}"
    return base64.b64encode(raw.encode("utf-8")).decode("utf-8")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username or not password:
        raise APIError("Username and password are required", 400)

    user = User.query.filter_by(username=username).first()
    if user is None or not user.check_password(password):
        logger.info("Failed login attempt for username=%s", username)
        raise APIError("Invalid username or password", 401)

    token = _issue_fake_token(user)
    logger.info("User %s logged in", username)

    return jsonify({"token": token, "user": user.to_dict()}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify(g.current_user.to_dict()), 200
