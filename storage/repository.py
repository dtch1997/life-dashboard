"""Concrete implementation of StorageInterface using SQLAlchemy."""

import json
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional

from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker

from interfaces import StorageInterface
from storage.database import get_engine, init_db
from storage.models import StoredObject


class SQLAlchemyStorageRepository(StorageInterface):
    """SQLAlchemy-based storage repository.

    Args:
        engine: Optional SQLAlchemy engine. If not provided, uses default from get_engine()
    """

    def __init__(self, engine: Optional[Engine] = None):
        """Initialize repository with optional engine."""
        self.engine = engine or get_engine()
        init_db(self.engine)

    @contextmanager
    def _session(self) -> Generator[Session, None, None]:
        """Create a database session using the repository's engine."""
        SessionLocal = sessionmaker(bind=self.engine)
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def store_object(self, object_type: str, data: Dict[str, Any]) -> int:
        """Store an object as JSON.

        Args:
            object_type: Type identifier (e.g., "radar_snapshot", "habit", "win")
            data: Dictionary to store as JSON

        Returns:
            ID of the created object
        """
        with self._session() as session:
            obj = StoredObject(
                object_type=object_type,
                data=json.dumps(data),
                created_at=datetime.now(),
            )
            session.add(obj)
            session.flush()
            assert obj.id is not None
            return int(obj.id)

    def get_objects(
        self,
        object_type: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve objects by type.

        Args:
            object_type: Type identifier to filter by
            limit: Maximum number of objects to return
            offset: Number of objects to skip

        Returns:
            List of deserialized objects
        """
        with self._session() as session:
            query = session.query(StoredObject).filter_by(object_type=object_type)
            query = query.order_by(StoredObject.created_at.desc())

            if offset:
                query = query.offset(offset)
            if limit:
                query = query.limit(limit)

            objects = query.all()
            return [json.loads(obj.data) for obj in objects]

    def get_object(self, object_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single object by ID.

        Args:
            object_id: ID of the object to retrieve

        Returns:
            Deserialized object data, or None if not found
        """
        with self._session() as session:
            obj = session.query(StoredObject).filter_by(id=object_id).first()
            return json.loads(obj.data) if obj else None

    def update_object(self, object_id: int, data: Dict[str, Any]) -> bool:
        """Update an existing object.

        Args:
            object_id: ID of the object to update
            data: New data to store

        Returns:
            True if object was updated, False if not found
        """
        with self._session() as session:
            obj = session.query(StoredObject).filter_by(id=object_id).first()
            if obj:
                obj.data = json.dumps(data)
                return True
            return False

    def delete_object(self, object_id: int) -> bool:
        """Delete an object by ID.

        Args:
            object_id: ID of the object to delete

        Returns:
            True if object was deleted, False if not found
        """
        with self._session() as session:
            obj = session.query(StoredObject).filter_by(id=object_id).first()
            if obj:
                session.delete(obj)
                return True
            return False

    def count_objects(self, object_type: str) -> int:
        """Count objects of a given type.

        Args:
            object_type: Type identifier to count

        Returns:
            Number of objects of the given type
        """
        with self._session() as session:
            return session.query(StoredObject).filter_by(object_type=object_type).count()

    def delete_objects_by_type(self, object_type: str) -> int:
        """Delete all objects of a given type.

        Args:
            object_type: Type identifier to delete

        Returns:
            Number of objects deleted
        """
        with self._session() as session:
            count = session.query(StoredObject).filter_by(object_type=object_type).delete()
            return count
