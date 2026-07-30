import logging

from flask import Blueprint, g, jsonify, request

from app.extensions import db
from app.models.comment import TaskComment
from app.models.task import Task
from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

# Registered under url_prefix="/api" (see app/routes/__init__.py) so the
# final paths are /api/tasks/<id>/comments, matching the tasks resource.
comments_bp = Blueprint("comments", __name__)


@comments_bp.route("/tasks/<int:task_id>/comments", methods=["GET"])
@login_required
def list_task_comments(task_id: int):
    task = Task.query.get(task_id)
    if task is None:
        raise APIError("Task not found", 404)

    comments = (
        TaskComment.query.filter_by(task_id=task_id)
        .order_by(TaskComment.created_at.asc())
        .all()
    )
    return jsonify([c.to_dict() for c in comments]), 200


@comments_bp.route("/tasks/<int:task_id>/comments", methods=["POST"])
@login_required
def create_task_comment(task_id: int):
    task = Task.query.get(task_id)
    if task is None:
        raise APIError("Task not found", 404)

    data = request.get_json(silent=True) or {}
    comment_text = (data.get("comment") or "").strip()
    if not comment_text:
        raise APIError("'comment' is required", 400)

    comment = TaskComment(
        task_id=task_id,
        user_id=g.current_user.id,
        comment=comment_text,
    )
    db.session.add(comment)
    db.session.commit()

    logger.info(
        "Comment added to task %s by user %s", task_id, g.current_user.username
    )
    return jsonify(comment.to_dict()), 201
