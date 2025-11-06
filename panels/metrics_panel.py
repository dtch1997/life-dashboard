"""
Quick Metrics panel - displays weekly statistics
"""

import streamlit as st
from typing import List, Tuple
from panels.base_panel import Panel


class MetricsPanel(Panel):
    """Panel displaying quick weekly metrics"""

    def __init__(self, metrics: List[Tuple[str, str]] = None):
        """
        Args:
            metrics: List of tuples (label, value)
        """
        self.metrics = metrics or self._get_mock_metrics()

    def _get_mock_metrics(self) -> List[Tuple[str, str]]:
        """Return mock metrics data"""
        return [
            ("Tasks completed", "23"),
            ("GitHub commits", "12"),
            ("Focus hours", "28")
        ]

    def render(self) -> None:
        """Render the Quick Metrics panel"""
        metrics_html = "\n".join([
            f"""<div style='text-align: center; padding: 15px 0; border-bottom: 1px solid rgba(102, 126, 234, 0.1);'>
                <div style='color: #667eea; font-size: 2em; font-weight: 300;'>{value}</div>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 5px;'>{label}</div>
            </div>"""
            for label, value in self.metrics
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
                '>📊 This Week</h3>
                <div>
                    {metrics_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
