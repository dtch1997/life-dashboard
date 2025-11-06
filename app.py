import streamlit as st
from datetime import datetime
from fetchers.todoist_fetcher import TodoistFetcher
from panels import (
    WinsPanel,
    GitHubPanel,
    MetricsPanel,
    FocusPanel,
    WeatherPanel,
    RadarPanel,
)

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

def main():
    # Sidebar greeting
    with st.sidebar:
        current_hour = datetime.now().hour

        # Time-based greeting
        if current_hour < 12:
            greeting = "Good morning"
            emoji = "🌅"
        elif current_hour < 17:
            greeting = "Good afternoon"
            emoji = "☀️"
        else:
            greeting = "Good evening"
            emoji = "🌙"

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
                '>{greeting}, Daniel</h2>
                <p style='
                    color: rgba(255,255,255,0.8);
                    font-size: 0.9em;
                    margin: 0;
                '>{datetime.now().strftime('%A, %B %d')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Main content area
    st.write("")

    # Life Radar - Full width panel
    # Mock radar data
    radar_ratings = {
        "Health/Fitness": 7,
        "Social Life": 6,
        "Relationships": 8,
        "Finances": 7,
        "Work/Career": 8,
    }
    RadarPanel(ratings=radar_ratings).render()

    st.write("")

    # Top row - 2 panels
    col1, col2 = st.columns(2)

    with col1:
        todoist = get_todoist_fetcher()
        WinsPanel(todoist_fetcher=todoist).render()

    with col2:
        GitHubPanel().render()

    st.write("")

    # Bottom row - 3 panels
    col1, col2, col3 = st.columns(3)

    with col1:
        MetricsPanel().render()

    with col2:
        FocusPanel().render()

    with col3:
        WeatherPanel().render()

if __name__ == "__main__":
    main()
