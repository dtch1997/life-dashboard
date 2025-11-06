import streamlit as st
from typing import Dict
from fetchers.todoist_fetcher import TodoistFetcher
from panels import (
    WinsPanel,
    RadarPanel,
    GreetingPanel,
)
from interfaces import StorageInterface
from storage.sqlalchemy import SQLAlchemyStorageRepository
from storage.models import RadarPanelData

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
    api_token = st.secrets.get("todoist_api_token", None)
    if api_token:
        return TodoistFetcher(api_token)
    return None


def get_default_ratings() -> Dict[str, int]:
    """Get default life radar ratings."""
    return {
        "Health/Fitness": 7,
        "Social Life": 6,
        "Relationships": 8,
        "Finances": 7,
        "Work/Career": 8,
    }


def load_radar_data(storage: StorageInterface) -> Dict[str, int]:
    """Load latest radar data from database.

    Args:
        storage: Storage interface for retrieving data

    Returns:
        Dictionary of dimension ratings, or defaults if no data exists
    """
    try:
        snapshots = storage.get_objects("radar_snapshot", limit=1)
        if snapshots:
            data = RadarPanelData(**snapshots[0])
            return data.ratings
    except Exception:
        # If there's any error loading data, fall back to defaults
        pass
    return get_default_ratings()


def main():
    # Initialize dependencies
    storage = get_storage()

    # Sidebar greeting
    with st.sidebar:
        GreetingPanel().render()

    # Main content area
    st.write("")

    # Initialize radar ratings in session state if not present
    if 'radar_ratings' not in st.session_state:
        st.session_state.radar_ratings = load_radar_data(storage)

    # 2-column layout: Today's Wins + Life Radar
    col1, col2 = st.columns(2)

    with col1:
        # Today's Wins panel
        todoist = get_todoist_fetcher()
        WinsPanel(todoist_fetcher=todoist).render()

    with col2:
        # Life Radar panel
        RadarPanel(ratings=st.session_state.radar_ratings).render()

if __name__ == "__main__":
    main()
