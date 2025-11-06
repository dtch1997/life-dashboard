"""
Habits panel - displays habit tracking with completion counts
"""

import streamlit as st
from datetime import datetime
from typing import List
from panels.base_panel import Panel
from pydantic import BaseModel, Field


class HabitData(BaseModel):
    """Type-safe data model for a single habit.

    Attributes:
        name: Name of the habit
        completions: List of completion timestamps
        target_frequency: Target frequency (e.g., "daily", "weekly")
        emoji: Optional emoji icon
    """

    name: str = Field(..., description="Habit name")
    completions: List[datetime] = Field(default_factory=list, description="Completion timestamps")
    target_frequency: str = Field(default="daily", description="Target frequency")
    emoji: str = Field(default="✓", description="Emoji icon")


class HabitsPanel(Panel):
    """Panel displaying habit tracking with completion counts"""

    def __init__(self, habits: List[HabitData], title: str = "Habits"):
        """
        Args:
            habits: List of HabitData objects
            title: Panel title
        """
        self.habits = habits
        self.title = title

    def render(self) -> None:
        """Render the Habits panel"""
        if not self.habits:
            st.markdown(
                f"""
                <div style='
                    padding: 25px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 15px;
                    border-left: 4px solid #667eea;
                '>
                    <h3 style='
                        color: #667eea;
                        margin-top: 0;
                        margin-bottom: 20px;
                        font-weight: 400;
                        font-size: 1.3em;
                    '>{self.title}</h3>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.95em;'>
                        No habits tracked yet. Start building consistency!
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            return

        # Build habits HTML
        habit_items = []
        for habit in self.habits:
            count = len(habit.completions)
            last_completion = max(habit.completions) if habit.completions else None
            last_text = last_completion.strftime("%b %d") if last_completion else "Never"

            # Color based on completion count
            if count >= 7:
                color = "#4CAF50"  # Green - strong streak
            elif count >= 3:
                color = "#667eea"  # Purple - building
            elif count >= 1:
                color = "#FF9800"  # Orange - starting
            else:
                color = "#666"     # Gray - no completions

            habit_html = f"<div style='padding: 15px; margin-bottom: 12px; background: rgba(255,255,255,0.03); border-radius: 10px; border-left: 4px solid {color}; display: flex; justify-content: space-between; align-items: center;'><div style='flex: 1;'><div style='color: #fafafa; font-size: 1em; font-weight: 500;'>{habit.emoji} {habit.name}</div><div style='color: rgba(255,255,255,0.5); font-size: 0.85em; margin-top: 4px;'>Last: {last_text}</div></div><div style='background: {color}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600; font-size: 0.95em;'>{count}x</div></div>"
            habit_items.append(habit_html)

        habits_html = "\n".join(habit_items)

        st.markdown(
            f"""
            <div style='
                padding: 25px;
                background: rgba(102, 126, 234, 0.1);
                border-radius: 15px;
                border-left: 4px solid #667eea;
            '>
                <h3 style='
                    color: #667eea;
                    margin-top: 0;
                    margin-bottom: 20px;
                    font-weight: 400;
                    font-size: 1.3em;
                '>{self.title}</h3>
                <div>
                    {habits_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
