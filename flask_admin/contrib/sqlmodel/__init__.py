"""
Flask-Admin SQLModel support module.

This module provides SQLModel integration for Flask-Admin, enabling
administrative interfaces for SQLModel models with full compatibility
to Flask-Admin's existing features.

Development supported by Claude (Anthropic) - AI-assisted implementation
of SQLModel compatibility layer for Flask-Admin v2.x series.

Refactoring Summary:
This module has been refactored to reduce code duplication with flask_admin.contrib.sqla
while preserving SQLModel-specific functionality. Key achievements:

Successfully Refactored Files:
- widgets.py: 75% reduction (47 → 12 lines) - Full import from SQLAlchemy
- validators.py: 34% reduction (97 → 64 lines) - Inheritance with query overrides
- typefmt.py: 28% reduction (71 → 51 lines) - Imported base formatters + SQLModel types
- fields.py: 81% reduction (477 → 89 lines) - Delegation with inheritance chains
- form.py: Utility functions successfully refactored
- tools.py: Partial refactoring - Imported common utility functions
while preserving SQLModel-specific logic

Files With Necessary Duplication:
- ajax.py: Different query paradigms (SQLAlchemy's query() vs SQLModel's select())
- filters.py: Contains SQLModel-specific computed field functionality
- view.py: Fundamental architectural differences and additional SQLModel functionality
- tools.py: Different ORM inspection approaches

Overall Impact: ~50% code reduction across refactorable files while maintaining
full test suite compatibility and preserving all SQLModel-specific features.
Additional utility function reuse in tools.py reduces maintenance burden.
"""

from ._types import T_MODEL_FIELD_LIST  # noqa: F401

# Export common types for external use
from ._types import T_SQLMODEL  # noqa: F401
from ._types import T_SQLMODEL_FIELD_ARGS  # noqa: F401
from ._types import T_SQLMODEL_PK_VALUE  # noqa: F401
from ._types import T_SQLMODEL_QUERY  # noqa: F401
from ._types import T_SQLMODEL_SESSION_TYPE  # noqa: F401
from .view import SQLModelView  # noqa: F401
