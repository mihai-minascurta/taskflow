"""
WSGI entrypoint.

Local development:
    flask --app wsgi run --debug --port 5000

Or run directly:
    python wsgi.py

Production-style serving (once containerized) would typically use a WSGI
server such as gunicorn, e.g.:
    gunicorn --bind 0.0.0.0:5000 wsgi:app
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app.config["PORT"], debug=app.config.get("DEBUG", False))
