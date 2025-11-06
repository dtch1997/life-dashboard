"""
Prototype of Life Radar Chart for Issue #2
Shows a visual snapshot of life dimensions with dummy data
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict
import random

# Page config
st.set_page_config(
    page_title="Life Radar Prototype",
    page_icon="🎯",
    layout="wide",
)


def generate_dummy_radar_data(date: datetime) -> Dict[str, int]:
    """Generate dummy ratings for each life dimension (1-10 scale)"""
    # Use date as seed for consistent but varied data
    random.seed(date.toordinal())

    dimensions = {
        "Health/Fitness": random.randint(5, 9),
        "Social Life": random.randint(4, 8),
        "Relationships": random.randint(6, 10),
        "Finances": random.randint(5, 8),
        "Work/Career": random.randint(6, 9),
    }
    return dimensions


def create_radar_chart(ratings: Dict[str, int], title: str = "Life Radar") -> go.Figure:
    """Create an interactive radar/spider chart from dimension ratings"""

    dimensions = list(ratings.keys())
    values = list(ratings.values())

    # Close the polygon by repeating the first value
    dimensions_plot = dimensions + [dimensions[0]]
    values_plot = values + [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_plot,
        theta=dimensions_plot,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=2),
        marker=dict(size=8, color='#667eea'),
        name='Current',
        hovertemplate='<b>%{theta}</b><br>Rating: %{r}/10<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickmode='linear',
                tick0=0,
                dtick=2,
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=12, color='rgba(255,255,255,0.6)'),
            ),
            angularaxis=dict(
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=13, color='#667eea'),
            ),
            bgcolor='rgba(0,0,0,0)',
        ),
        showlegend=False,
        title=dict(
            text=title,
            font=dict(size=20, color='#667eea'),
            x=0.5,
            xanchor='center',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=100, b=80),
        height=500,
    )

    return fig


def create_comparison_chart(
    current_ratings: Dict[str, int],
    previous_ratings: Dict[str, int],
) -> go.Figure:
    """Create radar chart comparing current vs previous snapshot"""

    dimensions = list(current_ratings.keys())
    current_values = list(current_ratings.values())
    previous_values = list(previous_ratings.values())

    # Close the polygon
    dimensions_plot = dimensions + [dimensions[0]]
    current_values_plot = current_values + [current_values[0]]
    previous_values_plot = previous_values + [previous_values[0]]

    fig = go.Figure()

    # Previous snapshot (lighter)
    fig.add_trace(go.Scatterpolar(
        r=previous_values_plot,
        theta=dimensions_plot,
        fill='toself',
        fillcolor='rgba(150, 150, 150, 0.2)',
        line=dict(color='rgba(150, 150, 150, 0.5)', width=2, dash='dot'),
        marker=dict(size=6, color='rgba(150, 150, 150, 0.5)'),
        name='Last Month',
        hovertemplate='<b>%{theta}</b><br>Last Month: %{r}/10<extra></extra>'
    ))

    # Current snapshot (vibrant)
    fig.add_trace(go.Scatterpolar(
        r=current_values_plot,
        theta=dimensions_plot,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color='#667eea'),
        name='Current',
        hovertemplate='<b>%{theta}</b><br>Current: %{r}/10<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickmode='linear',
                tick0=0,
                dtick=2,
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=12, color='rgba(255,255,255,0.6)'),
            ),
            angularaxis=dict(
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=13, color='#667eea'),
            ),
            bgcolor='rgba(0,0,0,0)',
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color='rgba(255,255,255,0.8)', size=12),
            bgcolor='rgba(0,0,0,0)',
        ),
        title=dict(
            text="Life Radar: Progress Comparison",
            font=dict(size=20, color='#667eea'),
            x=0.5,
            xanchor='center',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=100, b=100),
        height=550,
    )

    return fig


def display_dimension_cards(ratings: Dict[str, int]):
    """Display individual dimension cards with ratings and visual indicators"""

    # Emojis for each dimension
    dimension_emojis = {
        "Health/Fitness": "💪",
        "Social Life": "👥",
        "Relationships": "❤️",
        "Finances": "💰",
        "Work/Career": "🚀",
    }

    # Color coding based on rating
    def get_color(rating: int) -> str:
        if rating >= 8:
            return "#4CAF50"  # Green
        elif rating >= 6:
            return "#667eea"  # Purple (default)
        elif rating >= 4:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Red

    cols = st.columns(5)

    for idx, (dimension, rating) in enumerate(ratings.items()):
        with cols[idx]:
            color = get_color(rating)
            emoji = dimension_emojis.get(dimension, "📊")

            # Progress bar (out of 10)
            progress_pct = rating * 10

            st.markdown(
                f"""
                <div style='
                    padding: 20px;
                    background: rgba(102, 126, 234, 0.1);
                    border-radius: 12px;
                    border-left: 4px solid {color};
                    text-align: center;
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                '>
                    <div style='font-size: 2em;'>{emoji}</div>
                    <div style='
                        color: rgba(255,255,255,0.9);
                        font-size: 0.85em;
                        font-weight: 500;
                        margin: 8px 0;
                    '>{dimension}</div>
                    <div style='
                        color: {color};
                        font-size: 2.5em;
                        font-weight: 300;
                        margin: 5px 0;
                    '>{rating}</div>
                    <div style='
                        background: rgba(255,255,255,0.1);
                        border-radius: 10px;
                        height: 8px;
                        overflow: hidden;
                        margin-top: 10px;
                    '>
                        <div style='
                            background: {color};
                            height: 100%;
                            width: {progress_pct}%;
                            border-radius: 10px;
                            transition: width 0.3s ease;
                        '></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


def main():
    st.title("🎯 Life Radar Snapshot - Prototype")

    st.markdown(
        """
        <div style='
            padding: 20px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        '>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1em;'>
                This prototype demonstrates the <strong>Life Radar Chart</strong> feature from Issue #2.
                It provides a quick visual assessment of your life across 5 key dimensions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate dummy data
    today = datetime.now()
    current_ratings = generate_dummy_radar_data(today)
    previous_ratings = generate_dummy_radar_data(today - timedelta(days=30))

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Current Snapshot", "📈 Progress Over Time", "🎯 Dimension Details"])

    with tab1:
        st.markdown("### Current Life Radar")
        st.markdown(
            "<p style='color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Updated: Today</p>",
            unsafe_allow_html=True
        )

        # Main radar chart
        fig = create_radar_chart(current_ratings)
        st.plotly_chart(fig, use_container_width=True)

        # Summary stats
        avg_rating = sum(current_ratings.values()) / len(current_ratings)
        max_dim = max(current_ratings.items(), key=lambda x: x[1])
        min_dim = min(current_ratings.items(), key=lambda x: x[1])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 12px;'>
                    <div style='color: #667eea; font-size: 2.5em; font-weight: 300;'>{avg_rating:.1f}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Average Rating</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(76, 175, 80, 0.1); border-radius: 12px;'>
                    <div style='color: #4CAF50; font-size: 1.5em; font-weight: 500;'>{max_dim[0]}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Strongest ({max_dim[1]}/10)</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style='text-align: center; padding: 20px; background: rgba(255, 152, 0, 0.1); border-radius: 12px;'>
                    <div style='color: #FF9800; font-size: 1.5em; font-weight: 500;'>{min_dim[0]}</div>
                    <div style='color: rgba(255,255,255,0.7); font-size: 0.9em; margin-top: 8px;'>Needs Attention ({min_dim[1]}/10)</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab2:
        st.markdown("### Compare with Previous Snapshot")
        st.markdown(
            "<p style='color: rgba(255,255,255,0.7); margin-bottom: 20px;'>Current vs 30 days ago</p>",
            unsafe_allow_html=True
        )

        # Comparison chart
        fig = create_comparison_chart(current_ratings, previous_ratings)
        st.plotly_chart(fig, use_container_width=True)

        # Changes summary
        st.markdown("### Changes")
        changes_cols = st.columns(5)

        for idx, dimension in enumerate(current_ratings.keys()):
            current = current_ratings[dimension]
            previous = previous_ratings[dimension]
            delta = current - previous

            with changes_cols[idx]:
                delta_color = "#4CAF50" if delta > 0 else "#F44336" if delta < 0 else "rgba(255,255,255,0.6)"
                delta_symbol = "↑" if delta > 0 else "↓" if delta < 0 else "→"

                st.markdown(
                    f"""
                    <div style='text-align: center; padding: 15px; background: rgba(102, 126, 234, 0.1); border-radius: 10px;'>
                        <div style='color: rgba(255,255,255,0.8); font-size: 0.85em; margin-bottom: 8px;'>{dimension}</div>
                        <div style='color: {delta_color}; font-size: 1.8em; font-weight: 500;'>
                            {delta_symbol} {abs(delta)}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab3:
        st.markdown("### Dimension Breakdown")
        st.write("")

        # Individual dimension cards
        display_dimension_cards(current_ratings)

        st.write("")
        st.markdown("---")
        st.write("")

        # Mock historical trend for one dimension
        st.markdown("#### Sample Trend: Health/Fitness (Last 6 Months)")

        import plotly.express as px
        import pandas as pd

        # Generate mock historical data
        months = ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"]
        health_ratings = [6, 6, 7, 8, 7, current_ratings["Health/Fitness"]]

        df = pd.DataFrame({"Month": months, "Rating": health_ratings})

        fig_trend = px.line(
            df,
            x="Month",
            y="Rating",
            markers=True,
            range_y=[0, 10],
        )

        fig_trend.update_traces(
            line=dict(color='#667eea', width=3),
            marker=dict(size=10, color='#667eea')
        )

        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='rgba(255,255,255,0.8)'),
            xaxis=dict(
                gridcolor='rgba(102, 126, 234, 0.2)',
                title="",
            ),
            yaxis=dict(
                gridcolor='rgba(102, 126, 234, 0.2)',
                title="Rating",
            ),
            height=300,
        )

        st.plotly_chart(fig_trend, use_container_width=True)


if __name__ == "__main__":
    main()
