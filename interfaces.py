"""Core interfaces for dependency injection."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class StorageInterface(ABC):
    """Interface for storing and retrieving typed objects."""

    @abstractmethod
    def store_object(self, object_type: str, data: Dict[str, Any]) -> int:
        """Store an object as JSON.

        Args:
            object_type: Type identifier (e.g., "wheel_of_life_snapshot", "habit", "win")
            data: Dictionary to store as JSON

        Returns:
            ID of the created object
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_object(self, object_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve a single object by ID.

        Args:
            object_id: ID of the object to retrieve

        Returns:
            Deserialized object data, or None if not found
        """
        pass

    @abstractmethod
    def update_object(self, object_id: int, data: Dict[str, Any]) -> bool:
        """Update an existing object.

        Args:
            object_id: ID of the object to update
            data: New data to store

        Returns:
            True if object was updated, False if not found
        """
        pass

    @abstractmethod
    def delete_object(self, object_id: int) -> bool:
        """Delete an object by ID.

        Args:
            object_id: ID of the object to delete

        Returns:
            True if object was deleted, False if not found
        """
        pass

    @abstractmethod
    def count_objects(self, object_type: str) -> int:
        """Count objects of a given type.

        Args:
            object_type: Type identifier to count

        Returns:
            Number of objects of the given type
        """
        pass

    @abstractmethod
    def delete_objects_by_type(self, object_type: str) -> int:
        """Delete all objects of a given type.

        Args:
            object_type: Type identifier to delete

        Returns:
            Number of objects deleted
        """
        pass
