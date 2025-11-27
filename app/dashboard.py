# app/dashboard.py
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_BASE = "http://127.0.0.1:8000"


@st.cache_data
def fetch_games():
    resp = requests.get(f"{API_BASE}/games")
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


@st.cache_data
def fetch_team_metrics(window: int):
    resp = requests.get(f"{API_BASE}/team_metrics", params={"window": window})
    resp.raise_for_status()
    return pd.DataFrame(resp.json())


def main():
    st.set_page_config(page_title="NBA Team Metrics Dashboard", layout="wide")

    st.title("NBA Team Metrics Dashboard")
    st.caption("Data pipeline → FastAPI → Streamlit + Plotly")

    # Sidebar controls
    st.sidebar.header("Controls")
    window = st.sidebar.slider("Rolling window (games)", min_value=3, max_value=15, value=5, step=1)

    # Load data
    games_df = fetch_games()
    if games_df.empty:
        st.error("No games found. Run the pipeline first: `python -m app.pipeline`")
        return

    metrics_df = fetch_team_metrics(window)

    # BASIC INFO
    st.subheader("Game Log")
    st.dataframe(
        games_df.sort_values("game_date"),
        use_container_width=True,
        height=300,
    )

    # Points chart
    st.subheader("Points Scored vs Points Allowed")
    pts_df = games_df.copy()
    pts_df["game_date"] = pd.to_datetime(pts_df["game_date"])

    fig_pts = px.line(
        pts_df,
        x="game_date",
        y=["pts", "pts_allowed"],
        labels={"value": "Points", "variable": "Metric", "game_date": "Game Date"},
    )
    st.plotly_chart(fig_pts, use_container_width=True)

    # Rolling metrics chart
    st.subheader(f"Rolling Metrics (window = {window} games)")
    if not metrics_df.empty:
        metrics_df["game_date"] = pd.to_datetime(metrics_df["game_date"])

        fig_net = px.line(
            metrics_df,
            x="game_date",
            y=["avg_pts", "avg_pts_allowed", "net_rating"],
            labels={
                "value": "Value",
                "variable": "Metric",
                "game_date": "Game Date",
            },
        )
        st.plotly_chart(fig_net, use_container_width=True)
    else:
        st.info("Not enough games for rolling metrics yet.")


if __name__ == "__main__":
    main()
