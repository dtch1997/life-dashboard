import streamlit as st
from datetime import datetime
from typing import Dict, List
from fetchers.todoist_fetcher import TodoistFetcher
from panels import (
    WinsPanel,
    WheelOfLifePanel,
    GreetingPanel,
    HabitsPanel,
)
from panels.contribution_graph_panel import ContributionGraphPanel, generate_mock_contribution_data
from interfaces import StorageInterface
from storage.sqlalchemy import SQLAlchemyStorageRepository
from panels.wheel_of_life_panel import WheelOfLifeData
from panels.habits_panel import HabitData

# Page config
st.set_page_config(
    page_title="Life Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize storage
@st.cache_resource
def get_storage() -> StorageInterface:
    """Initialize storage repository."""
    return SQLAlchemyStorageRepository()


# Initialize Todoist fetcher
@st.cache_resource
def get_todoist_fetcher():
    """Initialize Todoist API client with token from secrets"""
    api_token = st.secrets["todoist_api_token"]
    return TodoistFetcher(api_token)


def get_default_ratings() -> Dict[str, int]:
    """Get default Wheel of Life ratings based on Ali Abdaal's framework.

    Ratings are on a 0-100 scale.
    """
    return {
        "Romance ❤️": 13,
        "Soul 🙏": 28,
        "Family 👨‍👩‍👧‍👦": 43,
        "Personal Growth 📈": 58,
        "Mind 🧠": 65,
        "Joy 😊": 73,
        "Body 💪": 73,
        "Friendships 🙌": 75,
        "Mission/Career 💼": 80,
        "Money 🤑": 85,
    }


def load_wheel_of_life_data(storage: StorageInterface) -> Dict[str, int]:
    """Load latest Wheel of Life data from database.

    Args:
        storage: Storage interface for retrieving data

    Returns:
        Dictionary of dimension ratings, or defaults if no data exists
    """
    try:
        snapshots = storage.get_objects("wheel_of_life_snapshot", limit=1)
        if snapshots:
            data = WheelOfLifeData(**snapshots[0])
            return data.ratings
    except Exception:
        # If there's any error loading data, fall back to defaults
        pass
    return get_default_ratings()


def get_default_habits() -> List[HabitData]:
    """Get default habit data for demonstration.

    Returns:
        List of HabitData with sample habits
    """
    return [
        HabitData(
            name="Post research update on Twitter",
            completions=[
                datetime(2025, 11, 4, 10, 0, 0),
                datetime(2025, 11, 6, 14, 0, 0),
            ],
            target_frequency="weekly",
            emoji="🐦"
        ),
    ]


def load_habits(storage: StorageInterface) -> List[HabitData]:
    """Load habits from database.

    Args:
        storage: Storage interface for retrieving data

    Returns:
        List of HabitData objects, or defaults if none exist
    """
    try:
        habit_records = storage.get_objects("habit", limit=10)
        if habit_records:
            habits = [HabitData(**record) for record in habit_records]
            return habits
    except Exception:
        # If there's any error loading data, fall back to defaults
        pass
    return get_default_habits()


def main():
    # Initialize dependencies
    storage = get_storage()

    # Sidebar greeting
    with st.sidebar:
        GreetingPanel().render()

    # Main content area
    st.write("")

    # Initialize Wheel of Life ratings in session state if not present
    if 'wheel_of_life_ratings' not in st.session_state:
        st.session_state.wheel_of_life_ratings = load_wheel_of_life_data(storage)

    # 2-column layout: Today's Wins + Wheel of Life
    col1, col2 = st.columns(2)

    with col1:
        # Contribution Graph panel
        contributions = get_todoist_fetcher().get_contribution_data(days=365)
        ContributionGraphPanel(contributions=contributions, title="🔥 Task Activity").render()

        # Today's Wins panel
        st.write("")
        WinsPanel(todoist_fetcher=get_todoist_fetcher()).render()

        # Habits panel
        st.write("")
        habits = load_habits(storage)
        HabitsPanel(habits=habits, title="📊 Habits").render()

    with col2:
        # Wheel of Life panel
        WheelOfLifePanel(ratings=st.session_state.wheel_of_life_ratings).render()

if __name__ == "__main__":
    main()
