"""Generic JSON storage layer using SQLAlchemy."""

from storage.models import Base, StoredObject
from storage.database import get_engine, get_session, init_db
from storage.crud import (
    store_object,
    get_objects,
    get_object,
    update_object,
    delete_object,
    count_objects,
    delete_objects_by_type,
)

__all__ = [
    # Models
    "Base",
    "StoredObject",
    # Database
    "get_engine",
    "get_session",
    "init_db",
    # CRUD
    "store_object",
    "get_objects",
    "get_object",
    "update_object",
    "delete_object",
    "count_objects",
    "delete_objects_by_type",
]
