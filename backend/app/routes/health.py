"""
Health check endpoint.

Intended to be used by DevOps tooling later on — e.g. a Kubernetes
liveness/readiness probe or a load balancer health check. Returns 200 with
DB connectivity status when healthy, and 503 if the database is
unreachable so an orchestrator knows to stop routing traffic here.
"""

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify
from sqlalchemy import text

from app.extensions import db

logger = logging.getLogger(__name__)

health_bp = Blueprint("health", __name__)

APP_VERSION = "1.0.0"


@health_bp.route("/health", methods=["GET"])
def health():
    db_status = "connected"
    http_status = 200

    try:
        db.session.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001 - deliberately broad, this is a health check
        logger.error("Health check DB connectivity failure: %s", exc)
        db_status = "unreachable"
        http_status = 503

    payload = {
        "status": "ok" if db_status == "connected" else "degraded",
        "version": APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
    }
    return jsonify(payload), http_status
