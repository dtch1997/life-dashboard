import streamlit as st
from datetime import datetime
from fetchers.todoist_fetcher import TodoistFetcher

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

    # Top row - 2 panels
    col1, col2 = st.columns(2)

    with col1:
        # Today's Wins panel - tasks completed today with priority 1 (p1)
        todoist = get_todoist_fetcher()

        if todoist:
            # Priority 4 = p1 in Todoist (highest priority)
            tasks = todoist.get_completed_today(priority=4)
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

        wins_html = "\n".join([f"<div style='padding: 8px 0; border-bottom: 1px solid rgba(102, 126, 234, 0.1);'>✓ {win}</div>" for win in wins])

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

    with col2:
        # GitHub Activity panel
        commits = [
            ("life-dashboard", "Add wins panel styling", "2h ago"),
            ("ml-experiments", "Optimize training loop", "5h ago"),
            ("dotfiles", "Update vim config", "1d ago"),
        ]

        commits_html = "\n".join([
            f"""<div style='padding: 12px 0; border-bottom: 1px solid rgba(102, 126, 234, 0.1);'>
                <div style='color: #667eea; font-size: 0.85em; font-weight: 500;'>{repo}</div>
                <div style='color: #fafafa; font-size: 0.95em; margin: 4px 0;'>{message}</div>
                <div style='color: rgba(255,255,255,0.5); font-size: 0.8em;'>{time}</div>
            </div>"""
            for repo, message, time in commits
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

    st.write("")

    # Bottom row - 3 panels
    col1, col2, col3 = st.columns(3)

    with col1:
        # Quick metrics
        metrics = [
            ("Tasks completed", "23"),
            ("GitHub commits", "12"),
            ("Focus hours", "28")
        ]

        metrics_html = "\n".join([
            f"""<div style='text-align: center; padding: 15px 0; border-bottom: 1px solid rgba(102, 126, 234, 0.1);'>
                <div style='color: #667eea; font-size: 2em; font-weight: 300;'>{value}</div>
                <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 5px;'>{label}</div>
            </div>"""
            for label, value in metrics
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

    with col2:
        # Current focus
        st.markdown(
            """
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
                    <div style='color: #fafafa; font-size: 1.2em; margin-bottom: 10px;'>Q4 Planning & Dashboard MVP</div>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.9em;'>Due: Nov 15</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        # Weather/mood
        st.markdown(
            """
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
                '>🌤️ Today</h3>
                <div style='text-align: center; padding: 20px 0;'>
                    <div style='font-size: 3em; margin: 10px 0;'>⛅</div>
                    <div style='color: #fafafa; font-size: 1.5em;'>72°F</div>
                    <div style='color: rgba(255,255,255,0.6); font-size: 0.9em; margin-top: 5px;'>Partly Cloudy</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
