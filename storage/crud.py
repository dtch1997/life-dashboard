"""CRUD operations for generic JSON storage."""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional

from storage.database import get_session
from storage.models import StoredObject


def store_object(object_type: str, data: Dict[str, Any]) -> int:
    """Store an object as JSON.

    Args:
        object_type: Type identifier (e.g., "radar_snapshot", "habit", "win")
        data: Dictionary to store as JSON

    Returns:
        ID of the created object

    Example:
        >>> data = {"dimension": "Health", "rating": 8}
        >>> obj_id = store_object("radar_snapshot", data)
    """
    with get_session() as session:
        obj = StoredObject(
            object_type=object_type,
            data=json.dumps(data),
            created_at=datetime.now(),
        )
        session.add(obj)
        session.flush()  # Get ID before commit
        return obj.id


def get_objects(
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

    Example:
        >>> snapshots = get_objects("radar_snapshot", limit=10)
        >>> for snap in snapshots:
        ...     print(snap["dimension"], snap["rating"])
    """
    with get_session() as session:
        query = session.query(StoredObject).filter_by(object_type=object_type)
        query = query.order_by(StoredObject.created_at.desc())

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        objects = query.all()
        return [json.loads(obj.data) for obj in objects]


def get_object(object_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single object by ID.

    Args:
        object_id: ID of the object to retrieve

    Returns:
        Deserialized object data, or None if not found

    Example:
        >>> data = get_object(123)
        >>> if data:
        ...     print(data["dimension"])
    """
    with get_session() as session:
        obj = session.query(StoredObject).filter_by(id=object_id).first()
        return json.loads(obj.data) if obj else None


def update_object(object_id: int, data: Dict[str, Any]) -> bool:
    """Update an existing object.

    Args:
        object_id: ID of the object to update
        data: New data to store

    Returns:
        True if object was updated, False if not found

    Example:
        >>> updated = update_object(123, {"dimension": "Health", "rating": 9})
    """
    with get_session() as session:
        obj = session.query(StoredObject).filter_by(id=object_id).first()
        if obj:
            obj.data = json.dumps(data)
            return True
        return False


def delete_object(object_id: int) -> bool:
    """Delete an object by ID.

    Args:
        object_id: ID of the object to delete

    Returns:
        True if object was deleted, False if not found

    Example:
        >>> deleted = delete_object(123)
    """
    with get_session() as session:
        obj = session.query(StoredObject).filter_by(id=object_id).first()
        if obj:
            session.delete(obj)
            return True
        return False


def count_objects(object_type: str) -> int:
    """Count objects of a given type.

    Args:
        object_type: Type identifier to count

    Returns:
        Number of objects of the given type

    Example:
        >>> num_snapshots = count_objects("radar_snapshot")
    """
    with get_session() as session:
        return session.query(StoredObject).filter_by(object_type=object_type).count()


def delete_objects_by_type(object_type: str) -> int:
    """Delete all objects of a given type.

    Args:
        object_type: Type identifier to delete

    Returns:
        Number of objects deleted

    Example:
        >>> deleted = delete_objects_by_type("radar_snapshot")
    """
    with get_session() as session:
        count = session.query(StoredObject).filter_by(object_type=object_type).delete()
        return count
