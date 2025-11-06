"""
Current Focus panel - displays main focus and due date
"""

import streamlit as st
from typing import Optional
from panels.base_panel import Panel


class FocusPanel(Panel):
    """Panel displaying current focus area"""

    def __init__(self, focus_text: Optional[str] = None, due_date: Optional[str] = None):
        self.focus_text = focus_text or "Q4 Planning & Dashboard MVP"
        self.due_date = due_date or "Nov 15"

    def render(self) -> None:
        """Render the Current Focus panel"""
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
                '>🎯 Current Focus</h3>
                <div style='text-align: center; padding: 20px 0;'>
                    <div style='color: #fafafa; font-size: 1.2em; margin-bottom: 10px;'>{self.focus_text}</div>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.9em;'>Due: {self.due_date}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
