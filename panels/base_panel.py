"""
Base panel interface for Life Dashboard components
"""

from abc import ABC, abstractmethod


class Panel(ABC):
    """Abstract base class for dashboard panels"""

    @abstractmethod
    def render(self) -> None:
        """Render the panel to Streamlit"""
        pass
