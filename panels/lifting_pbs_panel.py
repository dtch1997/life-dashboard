"""
Lifting PBs panel - displays personal bests for weight lifting exercises
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict
from panels.base_panel import Panel
from pydantic import BaseModel, Field, field_validator
import re


class ExerciseRecord(BaseModel):
    """Single exercise record with weight and reps.

    Attributes:
        weight: Weight lifted (in kg, or 'Bodyweight')
        reps: Number of repetitions
        is_bodyweight: Whether this is a bodyweight exercise
    """
    weight: str = Field(..., description="Weight lifted (e.g., '70kg' or 'Bodyweight')")
    reps: int = Field(..., description="Number of repetitions")
    is_bodyweight: bool = Field(default=False)

    @field_validator('reps')
    @classmethod
    def validate_reps(cls, v: int) -> int:
        """Ensure reps are positive."""
        if v <= 0:
            raise ValueError(f"Reps must be positive, got {v}")
        return v


class LiftingData(BaseModel):
    """Type-safe data model for lifting records.

    Attributes:
        exercises: Dictionary mapping exercise names to records
        version: Data format version for future migrations
    """
    exercises: Dict[str, ExerciseRecord] = Field(..., description="Exercise records")
    version: str = Field(default="1.0")


class LiftingPBsPanel(Panel):
    """Panel displaying lifting personal bests as bar chart"""

    def __init__(self, exercises: Dict[str, ExerciseRecord], title: str = "Lifting PBs", bodyweight_kg: float = 95.0):
        """
        Args:
            exercises: Dictionary mapping exercise names to ExerciseRecord
            title: Panel title
            bodyweight_kg: Bodyweight in kg for bodyweight exercises (default: 95.0)
        """
        self.exercises = exercises
        self.title = title
        self.bodyweight_kg = bodyweight_kg

    @staticmethod
    def parse_markdown(markdown_content: str) -> Dict[str, ExerciseRecord]:
        """Parse lifting data from markdown format.

        Expected format:
        # Lifting
        - Squat: 70kg x 8
        - Bench: 60kg x 8
        - Push-up: Bodyweight x 15

        Args:
            markdown_content: Markdown string containing exercise data

        Returns:
            Dictionary mapping exercise names to ExerciseRecord
        """
        exercises = {}
        pattern = r'^-\s*([^:]+):\s*([^\s]+)\s+x\s+(\d+)'

        for line in markdown_content.strip().split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                name = match.group(1).strip()
                weight = match.group(2).strip()
                reps = int(match.group(3))
                is_bodyweight = weight.lower() == 'bodyweight'

                exercises[name] = ExerciseRecord(
                    weight=weight,
                    reps=reps,
                    is_bodyweight=is_bodyweight
                )

        return exercises

    def export_data(self) -> LiftingData:
        """Export current exercises as typed data model.

        Returns:
            LiftingData with current exercises and metadata
        """
        return LiftingData(exercises=self.exercises)

    def import_data(self, data: LiftingData) -> None:
        """Import exercises from data model.

        Args:
            data: LiftingData containing validated exercises
        """
        self.exercises = data.exercises

    def _calculate_volume(self, record: ExerciseRecord) -> float:
        """Calculate training volume (weight × reps).

        For bodyweight exercises, uses the bodyweight_kg attribute.

        Args:
            record: Exercise record

        Returns:
            Volume in kg×reps
        """
        if record.is_bodyweight:
            return self.bodyweight_kg * record.reps

        # Extract numeric weight from string like "70kg"
        weight_match = re.match(r'(\d+(?:\.\d+)?)', record.weight)
        if weight_match:
            weight = float(weight_match.group(1))
            return weight * record.reps
        return 0.0

    def _create_bar_chart(self) -> go.Figure:
        """Create bar chart showing exercise weights and reps"""
        exercise_names = list(self.exercises.keys())

        # Prepare data for chart
        weights = []
        reps_list = []
        colors = []
        hover_texts = []

        for name in exercise_names:
            record = self.exercises[name]
            reps_list.append(record.reps)

            if record.is_bodyweight:
                weights.append(self.bodyweight_kg)
                volume = self.bodyweight_kg * record.reps
                hover_texts.append(f"{name}<br>Bodyweight ({self.bodyweight_kg}kg) × {record.reps} reps<br>Volume: {volume:.0f}kg")
                colors.append('#FF9800')  # Orange for bodyweight
            else:
                # Extract numeric weight
                weight_match = re.match(r'(\d+(?:\.\d+)?)', record.weight)
                if weight_match:
                    weight = float(weight_match.group(1))
                    weights.append(weight)
                    volume = weight * record.reps
                    hover_texts.append(f"{name}<br>{record.weight} × {record.reps} reps<br>Volume: {volume:.0f}kg")
                    colors.append('#667eea')  # Purple for weighted
                else:
                    weights.append(0)
                    hover_texts.append(f"{name}<br>{record.weight} × {record.reps} reps")
                    colors.append('#667eea')

        fig = go.Figure()

        # Add bar chart for weights
        fig.add_trace(go.Bar(
            x=exercise_names,
            y=weights,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertext=hover_texts,
            hoverinfo='text',
            name='Weight'
        ))

        fig.update_layout(
            title=dict(
                text=self.title,
                font=dict(size=20, color='#667eea'),
                x=0.5,
                xanchor='center',
            ),
            xaxis=dict(
                title=dict(text='Exercise', font=dict(size=14, color='#667eea')),
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=12, color='rgba(255,255,255,0.8)'),
            ),
            yaxis=dict(
                title=dict(text='Weight (kg)', font=dict(size=14, color='#667eea')),
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=12, color='rgba(255,255,255,0.6)'),
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=80, r=40, t=80, b=80),
            height=400,
            showlegend=False,
        )

        return fig

    def render(self) -> None:
        """Render the Lifting PBs panel"""
        if not self.exercises:
            st.info("No lifting data available")
            return

        fig = self._create_bar_chart()
        st.plotly_chart(fig, use_container_width=True)

        # Display summary stats
        weighted_exercises = {
            name: record for name, record in self.exercises.items()
            if not record.is_bodyweight
        }
        bodyweight_exercises = {
            name: record for name, record in self.exercises.items()
            if record.is_bodyweight
        }

        col1, col2, col3 = st.columns(3)

        with col1:
            total_exercises = len(self.exercises)
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 12px;'>
                    <div style='color: #667eea; font-size: 2.5em; font-weight: 300;'>{total_exercises}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Total Exercises</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            if weighted_exercises:
                heaviest = max(weighted_exercises.items(),
                              key=lambda x: self._calculate_volume(x[1]))
                heaviest_name = heaviest[0]
                heaviest_record = heaviest[1]
                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 20px; background: rgba(76, 175, 80, 0.1); border-radius: 12px;'>
                        <div style='color: #4CAF50; font-size: 1.5em; font-weight: 500;'>{heaviest_name}</div>
                        <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Highest Volume ({heaviest_record.weight} × {heaviest_record.reps})</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div style='text-align: center; padding: 20px; background: rgba(76, 175, 80, 0.1); border-radius: 12px;'>
                        <div style='color: #4CAF50; font-size: 1.5em; font-weight: 500;'>-</div>
                        <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>No Weighted</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col3:
            bodyweight_count = len(bodyweight_exercises)
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(255, 152, 0, 0.1); border-radius: 12px;'>
                    <div style='color: #FF9800; font-size: 2.5em; font-weight: 300;'>{bodyweight_count}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Bodyweight</div>
                </div>
                """,
                unsafe_allow_html=True
            )
