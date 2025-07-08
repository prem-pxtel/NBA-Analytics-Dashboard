import pandas as pd
import os
from nba_api.stats.endpoints import playercareerstats
from datetime import datetime
import time

def extract_team_history(player_id, max_years=5):
    try:
        df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
        df = df[df["LEAGUE_ID"] == "00"][["SEASON_ID", "TEAM_ID"]]
        if df.empty:
            return []

        df["start_year"] = df["SEASON_ID"].apply(lambda x: int(x.split("-")[0]))
        cutoff = datetime.now().year - max_years
        df = df[df["start_year"] >= cutoff]
        if df.empty:
            return []

        df = df.sort_values("start_year")
        grouped = df.groupby("TEAM_ID")["start_year"]
        periods = grouped.agg(["min", "max"]).reset_index()
        periods.columns = ["team_id", "start_season", "end_season"]
        periods["player_id"] = player_id
        return periods[["player_id", "team_id", "start_season", "end_season"]].to_dict("records")
    except Exception as e:
        print(f"Failed for player {player_id}: {e}")
        return []

def save_player_team_history():
    players_csv = os.path.join("data", "players.csv")
    output_csv = os.path.join("data", "player_team_history.csv")
    
    players_df = pd.read_csv(players_csv)
    player_ids = players_df["player_id"].tolist()


    all_team_history = []
    for i, player_id in enumerate(player_ids, 1):
        records = extract_team_history(player_id)
        all_team_history.extend(records)
        print(f"{i}/{len(player_ids)}: Added {len(records)} team records for player_id {player_id}")
        time.sleep(0.6)  # to avoid hitting rate limits

    if all_team_history:
        df = pd.DataFrame(all_team_history)
        df.to_csv(output_csv, index=False)
        print(f"Saved {len(df)} records to {output_csv}")
    else:
        print("No team history data extracted.")

if __name__ == "__main__":
    save_player_team_history()
