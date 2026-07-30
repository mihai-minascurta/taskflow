"""
Application configuration.

All configuration is sourced from environment variables so the same code can
run unmodified across local, staging, and production environments. See
.env.example for the full list of supported variables.
"""

import os

from dotenv import load_dotenv

# Load a local .env file if present. In real deployments, environment
# variables are expected to be injected by the runtime (systemd, container
# orchestrator, etc.) rather than read from a file.
load_dotenv()


def _split_origins(raw: str) -> list[str]:
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


class Config:
    """Base configuration shared by all environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-not-for-production")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://taskflow_user:taskflow_pass@localhost:5432/taskflow_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        # Guards against stale connections when the DB restarts or an idle
        # connection is dropped by a load balancer / proxy in front of it.
        "pool_pre_ping": True,
    }

    CORS_ORIGINS = _split_origins(os.environ.get("CORS_ORIGINS", "http://localhost:5173"))

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

    PORT = int(os.environ.get("PORT", 5000))

    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL", "sqlite:///:memory:"
    )


CONFIG_BY_NAME = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    env_name = os.environ.get("FLASK_ENV", "development")
    return CONFIG_BY_NAME.get(env_name, DevelopmentConfig)
