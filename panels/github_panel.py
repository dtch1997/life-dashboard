"""
GitHub Activity panel - displays recent commits
"""

import streamlit as st
from typing import List, Tuple
from panels.base_panel import Panel


class GitHubPanel(Panel):
    """Panel displaying recent GitHub commits"""

    def __init__(self, commits: List[Tuple[str, str, str]] = None):
        """
        Args:
            commits: List of tuples (repo_name, commit_message, time_ago)
        """
        self.commits = commits or self._get_mock_commits()

    def _get_mock_commits(self) -> List[Tuple[str, str, str]]:
        """Return mock commit data"""
        return [
            ("life-dashboard", "Add wins panel styling", "2h ago"),
            ("ml-experiments", "Optimize training loop", "5h ago"),
            ("dotfiles", "Update vim config", "1d ago"),
        ]

    def render(self) -> None:
        """Render the GitHub Activity panel"""
        commits_html = "\n".join([
            f"""<div style='padding: 12px 0; border-bottom: 1px solid rgba(102, 126, 234, 0.1);'>
                <div style='color: #667eea; font-size: 0.85em; font-weight: 500;'>{repo}</div>
                <div style='color: #fafafa; font-size: 0.95em; margin: 4px 0;'>{message}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 0.8em;'>{time}</div>
            </div>"""
            for repo, message, time in self.commits
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
                '>💻 Code Activity</h3>
                <div>
                    {commits_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
