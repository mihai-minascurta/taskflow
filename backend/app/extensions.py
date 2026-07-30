"""
Shared extension instances.

Kept in their own module (rather than instantiated inside __init__.py) so
that models and routes can import `db` without triggering circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
cors = CORS()
