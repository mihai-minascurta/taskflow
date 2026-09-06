from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.users import users_bp
from app.routes.projects import projects_bp
from app.routes.tasks import tasks_bp
from app.routes.comments import comments_bp
from app.routes.chat import chat_bp


def register_blueprints(app) -> None:
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(comments_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")
