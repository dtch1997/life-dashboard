"""
Life Radar panel - displays life dimensions as radar chart
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict
from panels.base_panel import Panel
from pydantic import BaseModel, Field, field_validator


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


class RadarPanel(Panel):
    """Panel displaying life radar chart with dimension ratings"""

    def __init__(self, ratings: Dict[str, int], title: str = "Life Radar"):
        """
        Args:
            ratings: Dictionary mapping dimension names to ratings (1-10)
            title: Chart title
        """
        self.ratings = ratings
        self.title = title

    def export_data(self) -> RadarPanelData:
        """Export current ratings as typed data model.

        Returns:
            RadarPanelData with current ratings and metadata
        """
        return RadarPanelData(ratings=self.ratings)

    def import_data(self, data: RadarPanelData) -> None:
        """Import ratings from data model.

        Args:
            data: RadarPanelData containing validated ratings
        """
        self.ratings = data.ratings

    def _create_radar_chart(self) -> go.Figure:
        """Create an interactive radar/spider chart from dimension ratings"""
        dimensions = list(self.ratings.keys())
        values = list(self.ratings.values())

        # Close the polygon by repeating the first value
        dimensions_plot = dimensions + [dimensions[0]]
        values_plot = values + [values[0]]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values_plot,
            theta=dimensions_plot,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=2),
            marker=dict(size=8, color='#667eea'),
            name='Current',
            hovertemplate='<b>%{theta}</b><br>Rating: %{r}/10<extra></extra>'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickmode='linear',
                    tick0=0,
                    dtick=2,
                    gridcolor='rgba(102, 126, 234, 0.2)',
                    tickfont=dict(size=12, color='rgba(255,255,255,0.6)'),
                ),
                angularaxis=dict(
                    gridcolor='rgba(102, 126, 234, 0.2)',
                    tickfont=dict(size=13, color='#667eea'),
                ),
                bgcolor='rgba(0,0,0,0)',
            ),
            showlegend=False,
            title=dict(
                text=self.title,
                font=dict(size=20, color='#667eea'),
                x=0.5,
                xanchor='center',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=80, r=80, t=100, b=80),
            height=500,
        )

        return fig

    def render(self) -> None:
        """Render the Life Radar panel"""
        fig = self._create_radar_chart()
        st.plotly_chart(fig, use_container_width=True)

        # Display summary stats
        avg_rating = sum(self.ratings.values()) / len(self.ratings)
        max_dim = max(self.ratings.items(), key=lambda x: x[1])
        min_dim = min(self.ratings.items(), key=lambda x: x[1])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 12px;'>
                    <div style='color: #667eea; font-size: 2.5em; font-weight: 300;'>{avg_rating:.1f}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Average Rating</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(76, 175, 80, 0.1); border-radius: 12px;'>
                    <div style='color: #4CAF50; font-size: 1.5em; font-weight: 500;'>{max_dim[0]}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Strongest ({max_dim[1]}/10)</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(255, 152, 0, 0.1); border-radius: 12px;'>
                    <div style='color: #FF9800; font-size: 1.5em; font-weight: 500;'>{min_dim[0]}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Needs Attention ({min_dim[1]}/10)</div>
                </div>
                """,
                unsafe_allow_html=True
            )
