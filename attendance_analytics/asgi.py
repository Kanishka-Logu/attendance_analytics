"""ASGI entry point compatible with platforms expecting the repository name as the package."""

# This module exists to support deploy platforms (e.g. Render) that
# run something like: `uvicorn attendance_analytics.asgi`.

from attendance_project.asgi import application  # noqa: F401
