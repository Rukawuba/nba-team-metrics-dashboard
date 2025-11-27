# app/pipeline.py
import os
import sqlite3
from datetime import datetime

import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nba_team.db")


def get_team_id_by_abbrev(abbrev: str) -> int:
    """Return NBA team id given abbreviation like 'PHX' or 'BOS'."""
    all_teams = teams.get_teams()
    matches = [t for t in all_teams if t["abbreviation"].upper() == abbrev.upper()]
    if not matches:
        raise ValueError(f"No team found with abbreviation {abbrev}")
    return matches[0]["id"]


def fetch_team_games(team_abbrev: str, season: str = "2024-25") -> pd.DataFrame:
    """
    Fetch all regular season games for a team using nba_api.
    season format examples: '2024-25', '2023-24'
    """
    team_id = get_team_id_by_abbrev(team_abbrev)

    gamefinder = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id,
        season_nullable=season,
        season_type_nullable="Regular Season",
    )
    games = gamefinder.get_data_frames()[0]

    # Keep a clean subset
    cols = [
        "GAME_ID",
        "GAME_DATE",
        "MATCHUP",
        "WL",
        "PTS",
        "PTS_ALLOWED",
    ]

    # The opponent points can be derived or may appear as OPP_PTS in some endpoints.
    # If PTS_ALLOWED doesn't exist, compute it from score string if present.
    if "PTS_OPP" in games.columns:
        games["PTS_ALLOWED"] = games["PTS_OPP"]
    elif "PLUS_MINUS" in games.columns:
        # Approximation: PLUS_MINUS = PTS - OPP_PTS
        games["PTS_ALLOWED"] = games["PTS"] - games["PLUS_MINUS"]
    else:
        # Fallback: set to None
        games["PTS_ALLOWED"] = None

    games = games[["GAME_ID", "GAME_DATE", "MATCHUP", "WL", "PTS", "PTS_ALLOWED"]]

    games["GAME_DATE"] = pd.to_datetime(games["GAME_DATE"])

    return games.sort_values("GAME_DATE")


def init_db():
    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS team_games (
            game_id TEXT PRIMARY KEY,
            game_date TEXT,
            matchup TEXT,
            wl TEXT,
            pts INTEGER,
            pts_allowed INTEGER
        )
        """
    )

    conn.commit()
    conn.close()


def load_games_to_db(df: pd.DataFrame):
    conn = sqlite3.connect(DB_PATH)
    df_to_write = df.copy()
    df_to_write["game_date"] = df_to_write["GAME_DATE"].dt.strftime("%Y-%m-%d")

    df_to_write = df_to_write.rename(
        columns={
            "GAME_ID": "game_id",
            "GAME_DATE": "game_date_unused",
            "MATCHUP": "matchup",
            "WL": "wl",
            "PTS": "pts",
            "PTS_ALLOWED": "pts_allowed",
        }
    )

    df_to_write = df_to_write[["game_id", "game_date", "matchup", "wl", "pts", "pts_allowed"]]

    df_to_write.to_sql("team_games", conn, if_exists="replace", index=False)
    conn.close()


def run_pipeline(team_abbrev: str = "PHX", season: str = "2024-25"):
    print(f"[{datetime.now()}] Initializing DB...")
    init_db()
    print(f"[{datetime.now()}] Fetching games for {team_abbrev} {season} ...")
    df = fetch_team_games(team_abbrev, season)
    print(f"[{datetime.now()}] {len(df)} games fetched.")
    print(f"[{datetime.now()}] Loading into SQLite...")
    load_games_to_db(df)
    print(f"[{datetime.now()}] Done.")


if __name__ == "__main__":
    # Change to whatever team/season you want
    run_pipeline(team_abbrev="PHX", season="2024-25")
