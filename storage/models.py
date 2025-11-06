"""SQLAlchemy models for generic JSON storage and Pydantic data models."""

from datetime import datetime
from typing import Dict
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel, Field, field_validator

Base = declarative_base()


class StoredObject(Base):
    """Generic storage for any object as JSON.

    Attributes:
        id: Primary key
        object_type: Type identifier (e.g., "radar_snapshot", "habit", "win")
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


class RadarPanelData(BaseModel):
    """Type-safe data model for Life Radar ratings.

    Attributes:
        ratings: Dictionary mapping dimension names to ratings (1-10)
        timestamp: When this snapshot was created
        version: Data format version for future migrations
    """

    ratings: Dict[str, int] = Field(..., description="Dimension ratings (1-10)")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0")

    @field_validator('ratings')
    @classmethod
    def validate_ratings(cls, v: Dict[str, int]) -> Dict[str, int]:
        """Ensure all ratings are in valid range (1-10)."""
        for dimension, rating in v.items():
            if not isinstance(rating, int):
                raise ValueError(f"Rating for '{dimension}' must be an integer, got {type(rating)}")
            if not 1 <= rating <= 10:
                raise ValueError(f"Rating for '{dimension}' must be 1-10, got {rating}")
        return v
