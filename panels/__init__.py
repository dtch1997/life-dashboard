"""
Panel components for the Life Dashboard
"""

from panels.base_panel import Panel
from panels.wins_panel import WinsPanel
from panels.github_panel import GitHubPanel
from panels.metrics_panel import MetricsPanel
from panels.focus_panel import FocusPanel
from panels.weather_panel import WeatherPanel
from panels.radar_panel import RadarPanel
from panels.greeting_panel import GreetingPanel
from panels.habits_panel import HabitsPanel

__all__ = [
    "Panel",
    "WinsPanel",
    "GitHubPanel",
    "MetricsPanel",
    "FocusPanel",
    "WeatherPanel",
    "RadarPanel",
    "GreetingPanel",
    "HabitsPanel",
]
