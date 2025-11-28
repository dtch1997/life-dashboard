"""
Tests for Lifting PBs panel and data models
"""

import pytest
from panels.lifting_pbs_panel import LiftingPBsPanel, ExerciseRecord, LiftingData


def test_exercise_record_valid():
    """Test creating a valid exercise record"""
    record = ExerciseRecord(weight="70kg", reps=8)
    assert record.weight == "70kg"
    assert record.reps == 8
    assert record.is_bodyweight is False


def test_exercise_record_bodyweight():
    """Test creating a bodyweight exercise record"""
    record = ExerciseRecord(weight="Bodyweight", reps=15, is_bodyweight=True)
    assert record.weight == "Bodyweight"
    assert record.reps == 15
    assert record.is_bodyweight is True


def test_exercise_record_invalid_reps():
    """Test that negative reps raise validation error"""
    with pytest.raises(ValueError, match="Reps must be positive"):
        ExerciseRecord(weight="70kg", reps=-5)


def test_exercise_record_zero_reps():
    """Test that zero reps raise validation error"""
    with pytest.raises(ValueError, match="Reps must be positive"):
        ExerciseRecord(weight="70kg", reps=0)


def test_lifting_data_model():
    """Test the LiftingData model with multiple exercises"""
    exercises = {
        "Squat": ExerciseRecord(weight="70kg", reps=8),
        "Push-up": ExerciseRecord(weight="Bodyweight", reps=15, is_bodyweight=True)
    }
    data = LiftingData(exercises=exercises)
    assert len(data.exercises) == 2
    assert data.version == "1.0"


def test_parse_markdown_valid():
    """Test parsing valid markdown content"""
    markdown = """# Lifting
- Squat: 70kg x 8
- Bench: 60kg x 8
- Leg extension: 109kg x 15
- Push-up: Bodyweight x 15
- Pull-up: Bodyweight x 12
"""
    exercises = LiftingPBsPanel.parse_markdown(markdown)

    assert len(exercises) == 5
    assert "Squat" in exercises
    assert exercises["Squat"].weight == "70kg"
    assert exercises["Squat"].reps == 8
    assert exercises["Squat"].is_bodyweight is False

    assert "Push-up" in exercises
    assert exercises["Push-up"].weight == "Bodyweight"
    assert exercises["Push-up"].reps == 15
    assert exercises["Push-up"].is_bodyweight is True


def test_parse_markdown_empty():
    """Test parsing empty markdown content"""
    markdown = "# Lifting\n"
    exercises = LiftingPBsPanel.parse_markdown(markdown)
    assert len(exercises) == 0


def test_parse_markdown_malformed():
    """Test parsing markdown with malformed lines (should skip them)"""
    markdown = """# Lifting
- Squat: 70kg x 8
- Invalid line without proper format
- Bench: 60kg x 8
"""
    exercises = LiftingPBsPanel.parse_markdown(markdown)
    assert len(exercises) == 2
    assert "Squat" in exercises
    assert "Bench" in exercises


def test_calculate_volume():
    """Test volume calculation for weighted exercises"""
    exercises = {
        "Squat": ExerciseRecord(weight="70kg", reps=8),
    }
    panel = LiftingPBsPanel(exercises=exercises)
    volume = panel._calculate_volume(exercises["Squat"])
    assert volume == 560.0  # 70kg × 8


def test_calculate_volume_bodyweight():
    """Test volume calculation for bodyweight exercises uses bodyweight_kg"""
    exercises = {
        "Push-up": ExerciseRecord(weight="Bodyweight", reps=15, is_bodyweight=True)
    }
    panel = LiftingPBsPanel(exercises=exercises, bodyweight_kg=95.0)
    volume = panel._calculate_volume(exercises["Push-up"])
    assert volume == 1425.0  # 95kg × 15


def test_calculate_volume_decimal_weight():
    """Test volume calculation with decimal weights"""
    exercises = {
        "Bench": ExerciseRecord(weight="62.5kg", reps=6),
    }
    panel = LiftingPBsPanel(exercises=exercises)
    volume = panel._calculate_volume(exercises["Bench"])
    assert volume == 375.0  # 62.5kg × 6


def test_export_data():
    """Test exporting panel data to LiftingData model"""
    exercises = {
        "Squat": ExerciseRecord(weight="70kg", reps=8),
    }
    panel = LiftingPBsPanel(exercises=exercises)
    data = panel.export_data()

    assert isinstance(data, LiftingData)
    assert len(data.exercises) == 1
    assert "Squat" in data.exercises
    assert data.version == "1.0"


def test_import_data():
    """Test importing LiftingData into panel"""
    exercises = {
        "Squat": ExerciseRecord(weight="70kg", reps=8),
        "Bench": ExerciseRecord(weight="60kg", reps=8),
    }
    data = LiftingData(exercises=exercises)

    panel = LiftingPBsPanel(exercises={})
    assert len(panel.exercises) == 0

    panel.import_data(data)
    assert len(panel.exercises) == 2
    assert "Squat" in panel.exercises
    assert "Bench" in panel.exercises


def test_panel_initialization():
    """Test panel initialization with exercises"""
    exercises = {
        "Squat": ExerciseRecord(weight="70kg", reps=8),
    }
    panel = LiftingPBsPanel(exercises=exercises, title="My Lifts")

    assert panel.title == "My Lifts"
    assert len(panel.exercises) == 1


def test_parse_markdown_whitespace_handling():
    """Test that parser handles extra whitespace correctly"""
    markdown = """# Lifting
-   Squat:   70kg   x   8
-Bench:60kg x 8
"""
    exercises = LiftingPBsPanel.parse_markdown(markdown)

    assert len(exercises) == 2
    assert "Squat" in exercises
    assert "Bench" in exercises
    assert exercises["Squat"].weight == "70kg"
    assert exercises["Bench"].weight == "60kg"
