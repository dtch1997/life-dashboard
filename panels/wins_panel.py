"""
Today's Wins panel - displays completed p1 tasks from Todoist
"""

import streamlit as st
from typing import List, Optional
from panels.base_panel import Panel
from fetchers.todoist_fetcher import TodoistFetcher


class WinsPanel(Panel):
    """Panel displaying today's completed priority 1 tasks"""

    def __init__(self, todoist_fetcher: Optional[TodoistFetcher] = None):
        self.todoist_fetcher = todoist_fetcher

    def _get_wins(self) -> List[str]:
        """Fetch today's wins from Todoist or use mock data"""
        if self.todoist_fetcher:
            # Priority 4 = p1 in Todoist (highest priority)
            tasks = self.todoist_fetcher.get_completed_today(priority=4)
            wins = [task["content"] for task in tasks] if tasks else []
        else:
            # Fallback to mock data if no API token
            wins = [
                "Deployed new dashboard feature",
                "Completed morning workout routine",
                "Finished quarterly planning doc",
                "Fixed critical bug in production",
                "Read 2 chapters of current book"
            ]

        if not wins:
            wins = ["No p1 tasks completed today yet - keep going!"]

        return wins

    def render(self) -> None:
        """Render the Today's Wins panel"""
        wins = self._get_wins()
        wins_html = "\n".join([
            f"<div style='padding: 8px 0; border-bottom: 1px solid rgba(102, 126, 234, 0.1);'>✓ {win}</div>"
            for win in wins
        ])

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
                '>🏆 Today's Wins</h3>
                <div style='color: #fafafa; font-size: 0.95em;'>
                    {wins_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
