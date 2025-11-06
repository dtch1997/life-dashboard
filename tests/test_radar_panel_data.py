"""Tests for RadarPanelData Pydantic model."""

import pytest
from datetime import datetime
from pydantic import ValidationError
from panels.radar_panel import RadarPanelData


def test_valid_ratings():
    """Test that valid ratings are accepted."""
    data = RadarPanelData(
        ratings={
            "Health": 5,
            "Finances": 8,
            "Work": 10,
        }
    )
    assert data.ratings == {"Health": 5, "Finances": 8, "Work": 10}
    assert data.version == "1.0"
    assert isinstance(data.timestamp, datetime)


def test_invalid_rating_too_low():
    """Test that ratings below 1 are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RadarPanelData(
            ratings={
                "Health": 0,
                "Finances": 5,
            }
        )
    assert "must be 1-10" in str(exc_info.value)


def test_invalid_rating_too_high():
    """Test that ratings above 10 are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RadarPanelData(
            ratings={
                "Health": 11,
                "Finances": 5,
            }
        )
    assert "must be 1-10" in str(exc_info.value)


def test_invalid_rating_not_int():
    """Test that non-numeric ratings are rejected."""
    with pytest.raises(ValidationError) as exc_info:
        RadarPanelData(
            ratings={  # type: ignore[arg-type]
                "Health": "invalid",
                "Finances": 8,
            }
        )
    # Pydantic will fail to convert "invalid" to int
    assert "validation error" in str(exc_info.value).lower()


def test_export_to_json():
    """Test that data can be exported to JSON."""
    data = RadarPanelData(
        ratings={
            "Health": 7,
            "Finances": 8,
        }
    )
    json_str = data.model_dump_json()
    assert '"Health":7' in json_str
    assert '"Finances":8' in json_str
    assert '"version":"1.0"' in json_str


def test_import_from_json():
    """Test that data can be imported from JSON."""
    json_str = '{"ratings": {"Health": 6, "Finances": 9}, "timestamp": "2025-01-01T12:00:00", "version": "1.0"}'
    data = RadarPanelData.model_validate_json(json_str)
    assert data.ratings == {"Health": 6, "Finances": 9}
    assert data.version == "1.0"


def test_import_from_dict():
    """Test that data can be imported from dictionary."""
    data_dict = {
        "ratings": {"Health": 7, "Social": 8},
        "timestamp": "2025-01-01T12:00:00",
        "version": "1.0"
    }
    data = RadarPanelData(**data_dict)  # type: ignore[arg-type]
    assert data.ratings == {"Health": 7, "Social": 8}


def test_boundary_values():
    """Test that boundary values (1 and 10) are accepted."""
    data = RadarPanelData(
        ratings={
            "Health": 1,
            "Finances": 10,
        }
    )
    assert data.ratings["Health"] == 1
    assert data.ratings["Finances"] == 10


def test_empty_ratings_dict():
    """Test that empty ratings dictionary is accepted."""
    data = RadarPanelData(ratings={})
    assert data.ratings == {}


def test_custom_timestamp():
    """Test that custom timestamp can be provided."""
    custom_time = datetime(2025, 1, 1, 12, 0, 0)
    data = RadarPanelData(
        ratings={"Health": 7},
        timestamp=custom_time
    )
    assert data.timestamp == custom_time
