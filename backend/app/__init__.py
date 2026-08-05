"""
Application factory.

Using the factory pattern (`create_app`) rather than a bare module-level
`app` keeps configuration explicit and makes it straightforward to create
multiple app instances with different configs (e.g. for tests).
"""

import logging

from flask import Flask

from app.config import get_config
from app.extensions import cors, db
from app.routes import register_blueprints
from app.utils.errors import register_error_handlers
from app.utils.logger import configure_logging
from prometheus_flask_exporter import PrometheusMetrics

logger = logging.getLogger(__name__)



def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    PrometheusMetrics(app)

    configure_logging(app)

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    register_blueprints(app)
    register_error_handlers(app)

    with app.app_context():
        # In this version of the app, table creation is handled by
        # database/schema.sql. This call is a safety net for a fresh local
        # setup where schema.sql hasn't been run yet, and is a no-op if the
        # tables already exist.
        db.create_all()

    app.logger.info("TaskFlow API initialized (env=%s)", app.config.get("ENV", "unknown"))

    return app
