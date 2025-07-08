import pandas as pd
from nba_api.stats.endpoints import playercareerstats
import time
import os

def save_cleaned_player_team_history():
    players_csv = os.path.join("data", "players.csv")
    output_csv = os.path.join("data", "player_team_history.csv")

    players_df = pd.read_csv(players_csv)
    player_ids = players_df["player_id"].tolist()

    all_team_data = []

    for i, player_id in enumerate(player_ids):
        try:
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            df = career.get_data_frames()[0]

            # Convert SEASON_ID to numeric start year for sorting
            df["SEASON_SORT"] = df["SEASON_ID"].apply(lambda s: int(s.split("-")[0]))
            df = df.sort_values("SEASON_SORT", ascending=False)

            # Limit to last 5 unique seasons
            recent_seasons = df["SEASON_ID"].unique()[:5]
            df = df[df["SEASON_ID"].isin(recent_seasons)]

            # Remove aggregate "TOT" rows
            df = df[df["TEAM_ABBREVIATION"] != "TOT"]

            # Get numeric start_season
            df["start_season"] = df["SEASON_ID"].apply(lambda s: int(s.split("-")[0]))

            # Group by player and team_id to determine start and end seasons
            for team_id, group in df.groupby("TEAM_ID"):
                seasons = sorted(group["start_season"].tolist())
                all_team_data.append({
                    "player_id": player_id,
                    "team_id": int(team_id),
                    "start_season": seasons[0],
                    "end_season": seasons[-1]
                })

            print(f"{i+1}/{len(player_ids)}: Processed player_id {player_id}")
        except Exception as e:
            print(f"{i+1}/{len(player_ids)}: Failed for player {player_id}: {e}")
        time.sleep(0.6)  # Respectful delay between API calls

    pd.DataFrame(all_team_data).to_csv(output_csv, index=False)
    print(f"Saved cleaned team history to {output_csv}")

if __name__ == "__main__":
    save_cleaned_player_team_history()
