"""WSGI entry point compatible with platforms expecting the repository name as the package."""

# This module exists to support deploy platforms (e.g. Render) that
# run something like: `gunicorn attendance_analytics.wsgi`.

from attendance_project.wsgi import application  # noqa: F401
