# app/api.py
import os
import sqlite3
from typing import List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nba_team.db")

app = FastAPI(title="NBA Team Metrics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.get("/games")
def get_games() -> List[Dict]:
    """Return all games."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT game_id, game_date, matchup, wl, pts, pts_allowed
        FROM team_games
        ORDER BY game_date
        """
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@app.get("/team_metrics")
def get_team_metrics(window: int = 5) -> List[Dict]:
    """
    Simple rolling metrics over last `window` games:
    - avg_pts
    - avg_pts_allowed
    - net_rating (approx = avg_pts - avg_pts_allowed)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT game_date, pts, pts_allowed
        FROM team_games
        ORDER BY game_date
        """
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return []

    # build rolling metrics
    metrics = []
    pts_hist = []
    pts_allowed_hist = []

    for r in rows:
        pts_hist.append(r["pts"])
        pts_allowed_hist.append(r["pts_allowed"])

        if len(pts_hist) > window:
            pts_hist.pop(0)
            pts_allowed_hist.pop(0)

        avg_pts = sum(pts_hist) / len(pts_hist)
        avg_pts_allowed = sum(pts_allowed_hist) / len(pts_allowed_hist)
        net = avg_pts - avg_pts_allowed

        metrics.append(
            {
                "game_date": r["game_date"],
                "avg_pts": avg_pts,
                "avg_pts_allowed": avg_pts_allowed,
                "net_rating": net,
            }
        )

    return metrics
