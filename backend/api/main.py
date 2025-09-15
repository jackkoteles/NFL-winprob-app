from fastapi import FastAPI
from typing import List, Dict
import pandas as pd
from datetime import datetime

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/predictions")
def predictions(season: int = 2024, week: int = 5) -> List[Dict]:
    # Temporary hard-coded data to build the UI and pipeline later
    demo = [
        {
            "game_id": f"{season}-W{week:02d}-KC-BUF",
            "season": season,
            "week": week,
            "away_team": "BUF",
            "home_team": "KC",
            "p_home_win": 0.62,
            "model_version": "v0-stub"
        },
        {
            "game_id": f"{season}-W{week:02d}-DAL-PHI",
            "season": season,
            "week": week,
            "away_team": "DAL",
            "home_team": "PHI",
            "p_home_win": 0.58,
            "model_version": "v0-stub"
        }
    ]
    return demo

@app.get("/games")
def games(season: int = 2024, week: int = 5) -> List[Dict]:
    df = pd.read_csv("backend/data/games_demo.csv")
    out = df[(df["season"] == season) & (df["week"] == week)]
    return out.to_dict(orient="records")

@app.get("/predictions")
def predictions(season: int = 2024, week: int = 5) -> List[Dict]:
    try:
        df = pd.read_csv("backend/data/predictions_demo.csv")
    except FileNotFoundError:
        # Fallback if the pipeline hasn't been run yet
        df = pd.read_csv("backend/data/games_demo.csv").copy()
        df["p_home_win"] = 0.55
        df["model_version"] = "v0-stub"

    out = df[(df["season"] == season) & (df["week"] == week)]
    cols = ["game_id","season","week","away_team","home_team","p_home_win","model_version"]
    return out[cols].to_dict(orient="records")


@app.get("/metrics/latest")
def metrics_latest():
    return {
        "model_version": "v0-stub",
        "computed_at": datetime.utcnow().isoformat() + "Z",
        "split": "demo",
        "brier": None,
        "logloss": None,
        "auc": None,
        "notes": "Stub metrics; training not implemented yet."
    }

