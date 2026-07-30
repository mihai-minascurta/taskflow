import logging
from datetime import datetime

from flask import Blueprint, g, jsonify, request

from app.extensions import db
from app.models.project import Project
from app.models.task import VALID_PRIORITIES, VALID_STATUSES, Task
from app.models.user import User
from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

tasks_bp = Blueprint("tasks", __name__)


def _parse_due_date(raw_value):
    if not raw_value:
        return None
    try:
        return datetime.strptime(raw_value, "%Y-%m-%d").date()
    except ValueError:
        raise APIError("'due_date' must be in YYYY-MM-DD format", 400)


@tasks_bp.route("", methods=["GET"])
@login_required
def list_tasks():
    query = Task.query

    status = request.args.get("status")
    if status:
        if status not in VALID_STATUSES:
            raise APIError(f"'status' must be one of {VALID_STATUSES}", 400)
        query = query.filter_by(status=status)

    project_id = request.args.get("project_id")
    if project_id:
        query = query.filter_by(project_id=project_id)

    assigned_to = request.args.get("assigned_to")
    if assigned_to:
        query = query.filter_by(assigned_to=assigned_to)

    tasks = query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200


@tasks_bp.route("", methods=["POST"])
@login_required
def create_task():
    data = request.get_json(silent=True) or {}

    title = (data.get("title") or "").strip()
    if not title:
        raise APIError("'title' is required", 400)

    project_id = data.get("project_id")
    if not project_id or Project.query.get(project_id) is None:
        raise APIError("A valid 'project_id' is required", 400)

    status = data.get("status", "todo")
    if status not in VALID_STATUSES:
        raise APIError(f"'status' must be one of {VALID_STATUSES}", 400)

    priority = data.get("priority", "medium")
    if priority not in VALID_PRIORITIES:
        raise APIError(f"'priority' must be one of {VALID_PRIORITIES}", 400)

    assigned_to = data.get("assigned_to")
    if assigned_to is not None and User.query.get(assigned_to) is None:
        raise APIError(f"assigned_to {assigned_to} does not exist", 400)

    task = Task(
        project_id=project_id,
        title=title,
        description=(data.get("description") or "").strip() or None,
        status=status,
        priority=priority,
        assigned_to=assigned_to,
        due_date=_parse_due_date(data.get("due_date")),
    )
    db.session.add(task)
    db.session.commit()

    logger.info("Task %s created by user %s", task.id, g.current_user.username)
    return jsonify(task.to_dict()), 201


@tasks_bp.route("/<int:task_id>", methods=["GET"])
@login_required
def get_task(task_id: int):
    task = Task.query.get(task_id)
    if task is None:
        raise APIError("Task not found", 404)
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id: int):
    task = Task.query.get(task_id)
    if task is None:
        raise APIError("Task not found", 404)

    data = request.get_json(silent=True) or {}

    if "title" in data:
        title = (data.get("title") or "").strip()
        if not title:
            raise APIError("'title' cannot be empty", 400)
        task.title = title

    if "description" in data:
        task.description = (data.get("description") or "").strip() or None

    if "status" in data:
        status = data.get("status")
        if status not in VALID_STATUSES:
            raise APIError(f"'status' must be one of {VALID_STATUSES}", 400)
        task.status = status

    if "priority" in data:
        priority = data.get("priority")
        if priority not in VALID_PRIORITIES:
            raise APIError(f"'priority' must be one of {VALID_PRIORITIES}", 400)
        task.priority = priority

    if "assigned_to" in data:
        assigned_to = data.get("assigned_to")
        if assigned_to is not None and User.query.get(assigned_to) is None:
            raise APIError(f"assigned_to {assigned_to} does not exist", 400)
        task.assigned_to = assigned_to

    if "due_date" in data:
        task.due_date = _parse_due_date(data.get("due_date"))

    if "project_id" in data:
        project_id = data.get("project_id")
        if Project.query.get(project_id) is None:
            raise APIError(f"project_id {project_id} does not exist", 400)
        task.project_id = project_id

    db.session.commit()
    logger.info("Task %s updated by user %s", task.id, g.current_user.username)
    return jsonify(task.to_dict()), 200


@tasks_bp.route("/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id: int):
    task = Task.query.get(task_id)
    if task is None:
        raise APIError("Task not found", 404)

    db.session.delete(task)
    db.session.commit()
    logger.info("Task %s deleted by user %s", task_id, g.current_user.username)
    return jsonify({"message": "Task deleted"}), 200
