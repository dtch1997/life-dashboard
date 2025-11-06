"""
Weather panel - displays current weather
"""

import streamlit as st
from typing import Optional
from panels.base_panel import Panel


class WeatherPanel(Panel):
    """Panel displaying weather information"""

    def __init__(self, emoji: Optional[str] = None, temperature: Optional[str] = None, description: Optional[str] = None):
        self.emoji = emoji or "⛅"
        self.temperature = temperature or "72°F"
        self.description = description or "Partly Cloudy"

    def render(self) -> None:
        """Render the Weather panel"""
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
                '>🌤️ Today</h3>
                <div style='text-align: center; padding: 20px 0;'>
                    <div style='font-size: 3em; margin: 10px 0;'>{self.emoji}</div>
                    <div style='color: #fafafa; font-size: 1.5em;'>{self.temperature}</div>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.9em; margin-top: 5px;'>{self.description}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
