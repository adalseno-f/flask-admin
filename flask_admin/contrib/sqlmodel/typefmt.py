"""
SQLModel type formatters for Flask-Admin.

This module imports base formatters from SQLAlchemy version and adds
SQLModel-specific formatters for types like Python Enums and lists.
Most formatting logic is shared between SQLModel and SQLAlchemy.
"""

from enum import Enum

from flask_admin.contrib.sqla.typefmt import arrow_export_formatter
from flask_admin.contrib.sqla.typefmt import arrow_formatter
from flask_admin.contrib.sqla.typefmt import choice_formatter

# Import base formatters from SQLAlchemy version to avoid duplication
from flask_admin.contrib.sqla.typefmt import DEFAULT_FORMATTERS
from flask_admin.contrib.sqla.typefmt import EXPORT_FORMATTERS
from flask_admin.model.typefmt import list_formatter

from ..._types import T_MODEL_VIEW


def enum_formatter(view: T_MODEL_VIEW, enum_member: Enum, name: str) -> str:
    """
    Return the value of an Enum member.

    :param enum_member:
        The Enum member.
    """
    return enum_member.value


# Add SQLModel-specific formatters to the imported base
DEFAULT_FORMATTERS.update(
    {
        list: list_formatter,  # Support for generic Python lists
        Enum: enum_formatter,  # Support for Python enums
    }
)

# Re-export for backwards compatibility
__all__ = [
    "DEFAULT_FORMATTERS",
    "EXPORT_FORMATTERS",
    "enum_formatter",
    "arrow_formatter",
    "arrow_export_formatter",
    "choice_formatter",
]
