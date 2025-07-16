from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import time
import csv
from datetime import datetime

#Last 5 seasons
current_year = datetime.now().year
season_start_years = [year for year in range(current_year - 5, current_year)]

# Get current NBA players
print("Fetching current NBA players...")
current_players = players.get_active_players()

# Output CSV file
output_file = "player_season_stats.csv"
header = ["player_id", "team_id", "season_id", "points_per_game", "assists_per_game", "rebounds_per_game", "blocks_per_game"]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)

    for player in current_players:
        player_id = player['id']
        full_name = player['full_name']

        try:
            print(f"Fetching season stats for {full_name} (ID: {player_id})...")
            stats = playercareerstats.PlayerCareerStats(player_id=player_id)
            df = stats.get_data_frames()[0]

            for _, row in df.iterrows():
                season_str = row["SEASON_ID"]  # Format: "2020-21"
                season_start = int(season_str[:4])

                if season_start in season_start_years:
                    team_id = row["TEAM_ID"]
                    ppg = row["PTS"]
                    apg = row["AST"]
                    rpg = row["REB"]
                    bpg = row["BLK"]

                    writer.writerow([player_id, team_id, season_start, ppg, apg, rpg, bpg])

        except Exception as e:
            print(f"Error with {full_name}: {e}")
        time.sleep(0.6)  # 

print(f"\nDone. Data written to {output_file}")
