import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Life Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Center column layout
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Vertical spacing
        st.write("")
        st.write("")
        st.write("")

        # Main greeting card
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

        # Card container
        with st.container():
            st.markdown(
                f"""
                <div style='
                    text-align: center;
                    padding: 60px 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                '>
                    <h1 style='
                        color: white;
                        font-size: 3.5em;
                        margin: 0;
                        font-weight: 300;
                        letter-spacing: 2px;
                    '>{emoji}</h1>
                    <h2 style='
                        color: white;
                        font-size: 2.5em;
                        margin: 20px 0 10px 0;
                        font-weight: 300;
                    '>{greeting}, Daniel</h2>
                    <p style='
                        color: rgba(255,255,255,0.8);
                        font-size: 1.2em;
                        margin: 0;
                    '>{datetime.now().strftime('%A, %B %d, %Y')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
