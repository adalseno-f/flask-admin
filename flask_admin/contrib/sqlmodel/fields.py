"""
Form fields for SQLModel ORM integration.

This module provides SQLModel-specific form fields by inheriting from SQLAlchemy
fields and adapting primary key handling and Row object extraction for SQLModel's
query patterns. Most field logic is reused with SQLModel-specific overrides.
"""

from flask_admin._compat import text_type

# Import base classes and functions from SQLAlchemy version to avoid duplication
from flask_admin.contrib.sqla.fields import CheckboxListField as SQLACheckboxListField
from flask_admin.contrib.sqla.fields import get_field_id
from flask_admin.contrib.sqla.fields import get_obj_pk
from flask_admin.contrib.sqla.fields import HstoreForm
from flask_admin.contrib.sqla.fields import InlineHstoreList
from flask_admin.contrib.sqla.fields import InlineModelFormList
from flask_admin.contrib.sqla.fields import InlineModelOneToOneField
from flask_admin.contrib.sqla.fields import KeyValue
from flask_admin.contrib.sqla.fields import QuerySelectField as SQLAQuerySelectField
from flask_admin.contrib.sqla.fields import (
    QuerySelectMultipleField as SQLAQuerySelectMultipleField,
)

# Import InlineFieldList for compatibility
from flask_admin.model.fields import InlineFieldList

from .tools import get_primary_key


def get_pk_from_identity(obj):
    """
    Get primary key from SQLModel instance using tools.get_primary_key
    """
    # Handle Row objects (but not strings) - Row objects are sequences but not strings
    if (
        hasattr(obj, "__len__")
        and hasattr(obj, "__getitem__")
        and not isinstance(obj, (str, bytes))
    ):
        try:
            # Extract the actual model object from Row
            if len(obj) > 0:
                obj = obj[0]
        except (TypeError, IndexError):
            pass

    # Handle direct SQLModel instances
    if hasattr(obj, "__table__"):
        # It's a SQLModel instance
        model_class = obj.__class__
        pk_names = get_primary_key(model_class)

        if isinstance(pk_names, tuple):
            # Multiple primary keys
            key_values = []
            for pk_name in pk_names:
                key_values.append(getattr(obj, str(pk_name)))
            return ":".join(text_type(x) for x in key_values)
        else:
            # Single primary key
            return text_type(getattr(obj, str(pk_names)))

    # Fallback for other objects - try to get id attribute,
    # otherwise return the object itself
    return text_type(getattr(obj, "id", obj))


class QuerySelectField(SQLAQuerySelectField):
    """SQLModel version of QuerySelectField.

    Inherits from SQLAlchemy version but uses SQLModel-specific primary key handling.
    """

    def __init__(self, *args, get_pk=None, **kwargs):
        # Override get_pk default to use SQLModel-specific function
        if get_pk is None:
            get_pk = get_pk_from_identity
        super().__init__(*args, get_pk=get_pk, **kwargs)

    def _get_object_list(self):
        """Override to handle Row object extraction for SQLModel."""
        if self._object_list is None:
            query = self.query or self.query_factory()
            get_pk = self.get_pk

            objects = []
            for obj in query:
                # Extract actual model object from Row if needed
                actual_obj = obj
                if (
                    hasattr(obj, "__len__")
                    and hasattr(obj, "__getitem__")
                    and not isinstance(obj, (str, bytes))
                ):
                    try:
                        if len(obj) > 0:
                            actual_obj = obj[0]
                    except (TypeError, IndexError):
                        pass

                objects.append((text_type(get_pk(obj)), actual_obj))

            self._object_list = objects
        return self._object_list


class QuerySelectMultipleField(QuerySelectField):
    """SQLModel version of QuerySelectMultipleField.

    Inherits from SQLModel QuerySelectField to maintain proper inheritance chain.
    Delegates behavior to SQLAlchemy's QuerySelectMultipleField.
    """

    # Copy widget from SQLAlchemy version
    widget = SQLAQuerySelectMultipleField.widget

    def __init__(self, *args, default=None, **kwargs):
        # Use SQLAlchemy's multiple field default behavior
        if default is None:
            default = []
        super().__init__(*args, default=default, **kwargs)
        self._invalid_formdata = False

    def _get_data(self):
        # Use SQLAlchemy's multiple field data getter logic
        return SQLAQuerySelectMultipleField._get_data(self)

    def _set_data(self, data):
        # Use SQLAlchemy's multiple field data setter logic
        return SQLAQuerySelectMultipleField._set_data(self, data)

    data = property(_get_data, _set_data)

    def iter_choices(self):
        # Use SQLAlchemy's multiple field iter_choices logic
        return SQLAQuerySelectMultipleField.iter_choices(self)

    def process_formdata(self, valuelist):
        # Use SQLAlchemy's multiple field process_formdata logic
        return SQLAQuerySelectMultipleField.process_formdata(self, valuelist)

    def pre_validate(self, form):
        # Use SQLAlchemy's multiple field pre_validate logic
        return SQLAQuerySelectMultipleField.pre_validate(self, form)


class CheckboxListField(QuerySelectMultipleField):
    """SQLModel version of CheckboxListField.

    Inherits from SQLModel QuerySelectMultipleField
    to maintain proper inheritance chain.
    """

    # Copy widget from SQLAlchemy version
    widget = SQLACheckboxListField.widget  # type: ignore[assignment]

    def pre_validate(self, form):
        # Use SQLAlchemy's CheckboxListField pre_validate logic (no-op)
        return SQLACheckboxListField.pre_validate(self, form)

    def process_formdata(self, valuelist):
        # Use SQLAlchemy's CheckboxListField process_formdata logic
        return SQLACheckboxListField.process_formdata(self, valuelist)


# Re-export all other classes and functions for backwards compatibility
__all__ = [
    "QuerySelectField",
    "QuerySelectMultipleField",
    "CheckboxListField",
    "HstoreForm",
    "InlineHstoreList",
    "InlineModelFormList",
    "InlineModelOneToOneField",
    "InlineFieldList",
    "KeyValue",
    "get_pk_from_identity",
    "get_obj_pk",
    "get_field_id",
]
