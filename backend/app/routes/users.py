"""
User routes.

Read-only for this version of the app — user management (creating/editing
accounts) is out of scope. This endpoint mainly exists so the frontend can
populate "assign to" / "owner" dropdowns.
"""

from flask import Blueprint, jsonify

from app.models.user import User
from app.utils.decorators import login_required

users_bp = Blueprint("users", __name__)


@users_bp.route("", methods=["GET"])
@login_required
def list_users():
    users = User.query.order_by(User.full_name).all()
    return jsonify([u.to_dict() for u in users]), 200
