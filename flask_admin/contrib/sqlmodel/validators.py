"""
SQLModel validators for Flask-Admin forms.

This module provides SQLModel-specific validators by inheriting from SQLAlchemy
validators and overriding query methods to use SQLModel's select() syntax.
The base validation logic is reused while adapting for SQLModel's query patterns.
"""

import typing as t

from sqlmodel import select
from wtforms import ValidationError

# Import from main types module
from flask_admin._types import T_TRANSLATABLE

# Import common validators from SQLAlchemy version to avoid duplication
from flask_admin.babel import lazy_gettext
from flask_admin.contrib.sqla.validators import ItemsRequired
from flask_admin.contrib.sqla.validators import TimeZoneValidator
from flask_admin.contrib.sqla.validators import Unique as SQLAUnique
from flask_admin.contrib.sqla.validators import valid_color
from flask_admin.contrib.sqla.validators import valid_currency

# Import SQLModel-specific types
from flask_admin.contrib.sqlmodel._types import T_SQLMODEL_SESSION_TYPE


class Unique(SQLAUnique):
    """Checks field value unicity against specified table field.

    :param db_session:
        A SQLModel Session instance.
    :param model:
        The SQLModel model to check unicity against.
    :param column:
        The unique column.
    :param message:
        The error message.
    """

    def __init__(
        self,
        db_session: T_SQLMODEL_SESSION_TYPE,
        model: t.Any,  # Use loose typing like SQLAlchemy version
        column: t.Any,
        message: t.Optional[T_TRANSLATABLE] = None,
    ) -> None:
        # Override to accept model instance instead of model class type
        self.db_session = db_session  # type: ignore[assignment]
        self.model = model
        self.column = column
        self.message = message or lazy_gettext("Already exists.")

    def __call__(self, form: t.Any, field: t.Any) -> None:
        # databases allow multiple NULL values for unique columns
        if field.data is None:
            return

        try:
            # Override query logic to use SQLModel's select() syntax
            # instead of session.query()
            obj = self.db_session.exec(  # type: ignore[attr-defined]
                select(self.model).where(self.column == field.data)
            ).one()

            if not hasattr(form, "_obj") or not form._obj == obj:
                raise ValidationError(str(self.message))
        except ValidationError:
            # Re-raise validation errors
            raise
        except Exception:
            # No result found or other database error -
            # this is OK for uniqueness validation
            pass


# Re-export imported validators for backwards compatibility
__all__ = [
    "Unique",
    "ItemsRequired",
    "TimeZoneValidator",
    "valid_color",
    "valid_currency",
]
