"""
Greeting panel - displays time-based greeting in sidebar
"""

import streamlit as st
from datetime import datetime
from panels.base_panel import Panel


class GreetingPanel(Panel):
    """Panel displaying time-based greeting with current date"""

    def __init__(self, name: str = "Daniel"):
        self.name = name

    def _get_greeting(self) -> tuple[str, str]:
        """Determine greeting and emoji based on current time

        Returns:
            Tuple of (greeting_message, emoji)
        """
        current_hour = datetime.now().hour

        if current_hour < 12:
            return "Good morning", "🌅"
        elif current_hour < 17:
            return "Good afternoon", "☀️"
        else:
            return "Good evening", "🌙"

    def render(self) -> None:
        """Render the greeting panel"""
        greeting, emoji = self._get_greeting()
        current_date = datetime.now().strftime('%A, %B %d')

        st.markdown(
            f"""
            <div style='
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                margin-bottom: 20px;
            '>
                <h1 style='
                    color: white;
                    font-size: 2.5em;
                    margin: 0;
                    font-weight: 300;
                '>{emoji}</h1>
                <h2 style='
                    color: white;
                    font-size: 1.5em;
                    margin: 15px 0 5px 0;
                    font-weight: 300;
                '>{greeting}, {self.name}</h2>
                <p style='
                    color: rgba(255,255,255,0.8);
                    font-size: 0.9em;
                    margin: 0;
                '>{current_date}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
