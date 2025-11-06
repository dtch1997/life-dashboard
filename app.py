import streamlit as st
from datetime import datetime
from typing import Dict
from fetchers.todoist_fetcher import TodoistFetcher
from panels import (
    WinsPanel,
    RadarPanel,
    GreetingPanel,
)
from storage.crud import store_object, get_objects
from storage.models import RadarPanelData

# Page config
st.set_page_config(
    page_title="Life Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

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


def load_radar_data() -> Dict[str, int]:
    """Load latest radar data from database.

    Returns:
        Dictionary of dimension ratings, or defaults if no data exists
    """
    try:
        snapshots = get_objects("radar_snapshot", limit=1)
        if snapshots:
            data = RadarPanelData(**snapshots[0])
            return data.ratings
    except Exception:
        # If there's any error loading data, fall back to defaults
        pass
    return get_default_ratings()


def main():
    # Sidebar greeting
    with st.sidebar:
        GreetingPanel().render()

        # Manage Life Radar data
        with st.expander("📊 Manage Life Radar"):
            st.markdown("Update, save, and export your life radar data.")

            # Load current ratings
            if 'radar_ratings' not in st.session_state:
                st.session_state.radar_ratings = load_radar_data()

            # Sliders to update ratings
            st.markdown("#### Update Ratings (1-10)")
            for dimension in st.session_state.radar_ratings.keys():
                st.session_state.radar_ratings[dimension] = st.slider(
                    dimension,
                    min_value=1,
                    max_value=10,
                    value=st.session_state.radar_ratings[dimension],
                    key=f"slider_{dimension}"
                )

            col1, col2 = st.columns(2)

            with col1:
                # Save to database
                if st.button("💾 Save to Database"):
                    try:
                        panel = RadarPanel(ratings=st.session_state.radar_ratings)
                        data = panel.export_data()
                        store_object("radar_snapshot", data.model_dump())
                        st.success("✅ Saved to database!")
                    except Exception as e:
                        st.error(f"❌ Error saving: {e}")

            with col2:
                # Export to JSON
                try:
                    panel = RadarPanel(ratings=st.session_state.radar_ratings)
                    json_data = panel.export_data().model_dump_json(indent=2)
                    st.download_button(
                        label="⬇️ Export JSON",
                        data=json_data,
                        file_name=f"life_radar_{datetime.now().strftime('%Y-%m-%d')}.json",
                        mime="application/json"
                    )
                except Exception as e:
                    st.error(f"❌ Error exporting: {e}")

            # Import from JSON
            st.markdown("#### Import from JSON")
            uploaded_file = st.file_uploader("Upload radar data", type=['json'], key="radar_upload")
            if uploaded_file is not None:
                try:
                    json_content = uploaded_file.read().decode('utf-8')
                    imported_data = RadarPanelData.model_validate_json(json_content)
                    st.session_state.radar_ratings = imported_data.ratings
                    st.success("✅ Data imported! Don't forget to save to database.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error importing: {e}")

    # Main content area
    st.write("")

    # Initialize radar ratings in session state if not present
    if 'radar_ratings' not in st.session_state:
        st.session_state.radar_ratings = load_radar_data()

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
