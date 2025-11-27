NBA Team Metrics Dashboard 🏀

A full-stack basketball analytics project that demonstrates API integration, data engineering, backend development, and interactive visualization — all using real NBA data pulled via nba_api.

This project builds an end-to-end pipeline:

NBA API → ETL Pipeline → SQLite Database → FastAPI Backend → Streamlit Dashboard (Plotly)


The result is a fully functional Basketball Software Engineering system:
You extract NBA game stats, store them, serve them over an API, and build a front-end dashboard to visualize rolling team performance metrics.

🚀 Features
1. Data Pipeline (Python)

Pulls real NBA game data using nba_api

Cleans and transforms key fields

Stores data in SQLite (data/nba_team.db)

Team + season configurable (PHX, BOS, LAL, etc.)

2. Backend API (FastAPI)

Exposes two endpoints:

/games → full game log

/team_metrics?window=5 → rolling averages of:

Points scored

Points allowed

Net rating proxy

3. Streamlit Dashboard

Displays complete game log

Line chart of points scored vs allowed

Interactive rolling metrics visualization

Adjustable rolling window (3–15 games)

Built with Plotly for sleek visuals

🏗 Project Structure
nba-team-metrics-dashboard/
│
├── README.md               # You are here
├── requirements.txt        # Project dependencies
│
├── data/
│   └── nba_team.db         # SQLite database (created by pipeline)
│
├── app/
│   ├── __init__.py
│   ├── pipeline.py         # ETL: NBA API → SQLite
│   ├── api.py              # FastAPI backend
│   └── dashboard.py        # Streamlit frontend
│
└── venv/                   # Virtual environment (ignored in Git)

🔧 Tech Stack

This project uses a realistic, production-style stack:

Core

Python 3.10+

SQLite

FastAPI

Streamlit

Plotly

Data

nba_api

Pandas

SQLAlchemy (optional)

Dev Tools

VS Code

Uvicorn (server)

Virtual environment

📦 Installation
1. Clone the repo
git clone https://github.com/YOUR_USERNAME/nba-team-metrics-dashboard.git
cd nba-team-metrics-dashboard

2. Create a virtual environment
python3 -m venv venv


Activate:

Mac/Linux

source venv/bin/activate


Windows

venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

🛠 Running the Project (Local Full Stack)

This is your full workflow.

▶️ Step 1: Run the ETL Pipeline (pull NBA data)

Modify run_pipeline() in pipeline.py if you want a different team or season:

run_pipeline(team_abbrev="PHX", season="2024-25")


Then run:

python -m app.pipeline


This creates/updates:

data/nba_team.db

▶️ Step 2: Start the FastAPI Backend
uvicorn app.api:app --reload


API now lives at:

http://127.0.0.1:8000


Useful endpoints:

http://127.0.0.1:8000/games

http://127.0.0.1:8000/team_metrics?window=5

▶️ Step 3: Run the Streamlit Dashboard

Open a second terminal (activate venv again):

streamlit run app/dashboard.py


Dashboard opens at:

http://localhost:8501

📊 Dashboard Preview

Game log table

Points vs. points allowed chart

Rolling metrics chart (avg points, avg points allowed, net rating)

Interactive window slider (3–15 games)

📈 Future Enhancements (Roadmap)
Analytics

True offensive/defensive rating

Four Factors analysis

Lineup-based metrics

Win probability modeling

Play-by-play derived features

Data Pipeline

Expand to player-level stats

Add postseason support

Add caching to minimize API calls

Convert raw SQL to SQLAlchemy ORM models

Backend

Add /players and /advanced_metrics routes

Add filtering logic (home/away, opponent, date, etc.)

Add pagination + sorting

Frontend

Team selection dropdown

Shot charts (via play-by-play)

Opponent scout pages

Dark/light theme toggle

Deployment

Deploy FastAPI on Render/Fly.io

Deploy Streamlit on Streamlit Cloud

CI/CD via GitHub Actions
