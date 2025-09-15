from pathlib import Path
from datetime import datetime
import pandas as pd

# Paths
DATA = Path("backend/data")
GAMES_CSV = DATA / "games_demo.csv"
PREDS_CSV = DATA / "predictions_demo.csv"

def main():
    df = pd.read_csv(GAMES_CSV).copy()
    # Placeholder model: constant home advantage
    df["p_home_win"] = 0.55
    df["model_version"] = "v0-stub"
    df["generated_at"] = datetime.utcnow().isoformat() + "Z"
    out = df[["game_id","season","week","away_team","home_team","p_home_win","model_version","generated_at"]]
    PREDS_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(PREDS_CSV, index=False)
    print(f"Wrote {len(out)} predictions → {PREDS_CSV}")

if __name__ == "__main__":
    main()
