"""Generic JSON storage layer using SQLAlchemy."""

from storage.models import Base, StoredObject

__all__ = ["Base", "StoredObject"]
