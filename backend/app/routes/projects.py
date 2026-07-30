import logging

from flask import Blueprint, g, jsonify, request

from app.extensions import db
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.utils.decorators import login_required
from app.utils.errors import APIError

logger = logging.getLogger(__name__)

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("", methods=["GET"])
@login_required
def list_projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route("", methods=["POST"])
@login_required
def create_project():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()

    if not name:
        raise APIError("'name' is required", 400)

    owner_id = data.get("owner_id", g.current_user.id)
    if User.query.get(owner_id) is None:
        raise APIError(f"owner_id {owner_id} does not exist", 400)

    project = Project(
        name=name,
        description=(data.get("description") or "").strip() or None,
        owner_id=owner_id,
    )
    db.session.add(project)
    db.session.commit()

    logger.info("Project %s created by user %s", project.id, g.current_user.username)
    return jsonify(project.to_dict()), 201


@projects_bp.route("/<int:project_id>", methods=["GET"])
@login_required
def get_project(project_id: int):
    project = Project.query.get(project_id)
    if project is None:
        raise APIError("Project not found", 404)
    return jsonify(project.to_dict()), 200


@projects_bp.route("/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id: int):
    project = Project.query.get(project_id)
    if project is None:
        raise APIError("Project not found", 404)

    data = request.get_json(silent=True) or {}

    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            raise APIError("'name' cannot be empty", 400)
        project.name = name

    if "description" in data:
        project.description = (data.get("description") or "").strip() or None

    if "owner_id" in data:
        owner_id = data.get("owner_id")
        if User.query.get(owner_id) is None:
            raise APIError(f"owner_id {owner_id} does not exist", 400)
        project.owner_id = owner_id

    db.session.commit()
    logger.info("Project %s updated by user %s", project.id, g.current_user.username)
    return jsonify(project.to_dict()), 200


@projects_bp.route("/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id: int):
    project = Project.query.get(project_id)
    if project is None:
        raise APIError("Project not found", 404)

    db.session.delete(project)
    db.session.commit()
    logger.info("Project %s deleted by user %s", project_id, g.current_user.username)
    return jsonify({"message": "Project deleted"}), 200


@projects_bp.route("/<int:project_id>/tasks", methods=["GET"])
@login_required
def list_project_tasks(project_id: int):
    project = Project.query.get(project_id)
    if project is None:
        raise APIError("Project not found", 404)

    tasks = (
        Task.query.filter_by(project_id=project_id)
        .order_by(Task.created_at.desc())
        .all()
    )
    return jsonify([t.to_dict() for t in tasks]), 200
