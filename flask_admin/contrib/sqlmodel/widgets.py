"""
SQLModel widgets for Flask-Admin forms.

This module imports widgets from the SQLAlchemy version to avoid code duplication,
as the widget implementations are identical between SQLModel and SQLAlchemy.
"""

# Import widgets from SQLAlchemy version to avoid duplication
from flask_admin.contrib.sqla.widgets import CheckboxListInput

# Re-export for backwards compatibility
__all__ = ["CheckboxListInput"]
