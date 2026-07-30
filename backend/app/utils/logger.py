"""
Logging setup.

Deliberately simple: logs are written to stdout/stderr with a consistent
format and a configurable level. Shipping/aggregating these logs (e.g. to
CloudWatch, ELK, Loki) is left to the DevOps/infrastructure layer — the
application's job is just to emit them consistently.
"""

import logging
import sys


def configure_logging(app) -> None:
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"), logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(log_level)

    # Werkzeug's own request logger — align its level with ours.
    logging.getLogger("werkzeug").setLevel(log_level)

    app.logger.setLevel(log_level)
    app.logger.info("Logging configured at level %s", app.config.get("LOG_LEVEL", "INFO"))
