import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Life Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    st.write("")

    # Wins panel
    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        # Wins panel
        st.markdown(
            """
            <div style='
                padding: 20px;
                background: rgba(102, 126, 234, 0.1);
                border-radius: 15px;
                border-left: 4px solid #667eea;
            '>
                <h3 style='
                    color: #667eea;
                    margin-top: 0;
                    font-weight: 400;
                    font-size: 1.3em;
                '>🏆 Weekly Wins</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Mock completed tasks
        wins = [
            "Deployed new dashboard feature",
            "Completed morning workout routine",
            "Finished quarterly planning doc",
            "Fixed critical bug in production",
            "Read 2 chapters of current book"
        ]

        st.write("")
        for win in wins:
            st.markdown(
                f"""
                <div style='
                    padding: 10px 15px;
                    margin: 8px 0;
                    background: rgba(102, 126, 234, 0.05);
                    border-radius: 8px;
                    border-left: 3px solid #667eea;
                    color: #fafafa;
                    font-size: 0.95em;
                '>
                    ✓ {win}
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
