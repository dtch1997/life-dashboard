"""
Contribution Graph panel - displays GitHub-style activity heatmap
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict
from panels.base_panel import Panel
import random


def generate_mock_contribution_data(days: int = 365) -> Dict[str, int]:
    """Generate mock contribution data for the specified number of days.

    Args:
        days: Number of days to generate data for

    Returns:
        Dictionary mapping date strings (YYYY-MM-DD) to contribution counts
    """
    data = {}
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days - 1)

    current_date = start_date
    while current_date <= end_date:
        # Generate realistic-looking data with occasional bursts
        # Most days have 0-5 contributions, some have more
        rand = random.random()
        if rand < 0.2:  # 20% chance of no activity
            count = 0
        elif rand < 0.6:  # 40% chance of light activity
            count = random.randint(1, 3)
        elif rand < 0.85:  # 25% chance of moderate activity
            count = random.randint(4, 8)
        else:  # 15% chance of high activity
            count = random.randint(9, 20)

        data[current_date.strftime("%Y-%m-%d")] = count
        current_date += timedelta(days=1)

    return data


class ContributionGraphPanel(Panel):
    """Panel displaying GitHub-style contribution heatmap"""

    def __init__(self, contributions: Dict[str, int], title: str = "Activity"):
        """
        Args:
            contributions: Dictionary mapping date strings to contribution counts
            title: Panel title
        """
        self.contributions = contributions
        self.title = title

    def _calculate_streaks(self) -> tuple[int, int]:
        """Calculate current streak and longest streak.

        Returns:
            Tuple of (current_streak, longest_streak)
        """
        if not self.contributions:
            return 0, 0

        sorted_dates = sorted(self.contributions.keys(), reverse=True)

        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()
        check_date = today

        for i in range(len(sorted_dates)):
            date_str = check_date.strftime("%Y-%m-%d")
            if date_str in self.contributions and self.contributions[date_str] > 0:
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                break

        # Calculate longest streak
        longest_streak = 0
        temp_streak = 0

        for date_str in sorted(self.contributions.keys()):
            if self.contributions[date_str] > 0:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 0

        return current_streak, longest_streak

    def _create_contribution_heatmap(self) -> go.Figure:
        """Create a GitHub-style contribution heatmap"""
        if not self.contributions:
            # Return empty figure
            fig = go.Figure()
            fig.update_layout(
                title="No data available",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            return fig

        # Prepare data for heatmap
        sorted_dates = sorted(self.contributions.keys())
        start_date = datetime.strptime(sorted_dates[0], "%Y-%m-%d").date()
        end_date = datetime.strptime(sorted_dates[-1], "%Y-%m-%d").date()

        # Adjust start_date to previous Monday
        days_to_subtract = start_date.weekday()
        grid_start = start_date - timedelta(days=days_to_subtract)

        # Build grid: rows = days of week (Mon=0, Sun=6), cols = weeks
        weeks_data = []
        current_date = grid_start
        week_data = [None] * 7  # Monday to Sunday
        week_dates = [None] * 7
        weeks_dates = []

        while current_date <= end_date:
            day_of_week = current_date.weekday()  # Mon=0, Sun=6
            date_str = current_date.strftime("%Y-%m-%d")
            count = self.contributions.get(date_str, 0)

            week_data[day_of_week] = count
            week_dates[day_of_week] = date_str

            # If Sunday or last day, save the week
            if day_of_week == 6 or current_date == end_date:
                weeks_data.append(week_data[:])
                weeks_dates.append(week_dates[:])
                week_data = [None] * 7
                week_dates = [None] * 7

            current_date += timedelta(days=1)

        # Transpose for plotly (rows become columns)
        z_data = []
        hover_data = []
        for day in range(7):
            day_row = []
            hover_row = []
            for week in range(len(weeks_data)):
                count = weeks_data[week][day]
                date_str = weeks_dates[week][day]
                day_row.append(count if count is not None else 0)

                if date_str:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    hover_text = f"{date_obj.strftime('%b %d, %Y')}<br>{count if count else 0} contributions"
                else:
                    hover_text = ""
                hover_row.append(hover_text)
            z_data.append(day_row)
            hover_data.append(hover_row)

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=z_data,
            text=hover_data,
            hovertemplate='%{text}<extra></extra>',
            colorscale=[
                [0, 'rgba(102, 126, 234, 0.05)'],      # Very light purple
                [0.2, 'rgba(102, 126, 234, 0.3)'],     # Light purple
                [0.5, 'rgba(102, 126, 234, 0.6)'],     # Medium purple
                [0.8, 'rgba(102, 126, 234, 0.85)'],    # Dark purple
                [1, '#667eea']                          # Full purple
            ],
            showscale=False,
            xgap=3,
            ygap=3,
        ))

        # Update layout
        fig.update_layout(
            title=dict(
                text=self.title,
                font=dict(size=20, color='#667eea'),
                x=0,
                xanchor='left',
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                zeroline=False,
            ),
            yaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                ticktext=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                tickfont=dict(size=10, color='rgba(255,255,255,0.6)'),
                showgrid=False,
                zeroline=False,
                autorange='reversed',
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=60, r=20, t=60, b=20),
            height=200,
        )

        return fig

    def render(self) -> None:
        """Render the Contribution Graph panel"""
        # Display heatmap
        fig = self._create_contribution_heatmap()
        st.plotly_chart(fig, use_container_width=True)

        # Calculate statistics
        total = sum(self.contributions.values())
        avg_per_day = total / len(self.contributions) if self.contributions else 0
        current_streak, longest_streak = self._calculate_streaks()

        # Display summary stats
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 12px;'>
                    <div style='color: #667eea; font-size: 2em; font-weight: 300;'>{total}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.85em; margin-top: 6px;'>Total</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 15px; background: rgba(76, 175, 80, 0.1); border-radius: 12px;'>
                    <div style='color: #4CAF50; font-size: 2em; font-weight: 300;'>{current_streak}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.85em; margin-top: 6px;'>Current Streak</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 15px; background: rgba(255, 152, 0, 0.1); border-radius: 12px;'>
                    <div style='color: #FF9800; font-size: 2em; font-weight: 300;'>{longest_streak}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.85em; margin-top: 6px;'>Longest Streak</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 12px;'>
                    <div style='color: #667eea; font-size: 2em; font-weight: 300;'>{avg_per_day:.1f}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.85em; margin-top: 6px;'>Avg/Day</div>
                </div>
                """,
                unsafe_allow_html=True
            )
