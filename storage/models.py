"""SQLAlchemy models for generic JSON storage."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StoredObject(Base):
    """Generic storage for any object as JSON.

    Attributes:
        id: Primary key
        object_type: Type identifier (e.g., "wheel_of_life_snapshot", "habit", "win")
        data: JSON string containing the object data
        created_at: Timestamp when object was created
    """

    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    object_type = Column(String, nullable=False)
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    def __repr__(self) -> str:
        return f"<StoredObject(id={self.id}, type={self.object_type})>"
