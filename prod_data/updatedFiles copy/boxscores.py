import time
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2

def fetch_boxscores(season="2024-25", season_type="Regular Season", delay=0.6, output_file="data/boxscores.csv", player_file="data/players.csv", game_file="data/games.csv"):
    # Load valid player and game IDs
    valid_player_ids = set(pd.read_csv(player_file)["player_id"].unique())
    valid_game_ids = set(pd.read_csv(game_file)["GAME_ID"].astype(int).unique())

    # Get all games from the season
    print("Fetching NBA games...")
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable=season_type)
    games_df = gamefinder.get_data_frames()[0]
    
    # Convert GAME_IDs to integers (strip leading zeros)
    game_ids = games_df['GAME_ID'].astype(int).unique()

    print(f"Found {len(game_ids)} games. Downloading box scores...")

    initialized = False

    for idx, game_id in enumerate(game_ids, 1):
        # Skip games not in filtered games.csv
        if game_id not in valid_game_ids:
            continue

        try:
            # API expects 10-digit string
            boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=str(game_id).zfill(10))
            stats_df = boxscore.player_stats.get_data_frame()

            # Filter out DNP players 
            stats_df = stats_df[stats_df["MIN"].notna() & (stats_df["MIN"] != "0")]

            # Select and rename columns
            selected = stats_df[[
                "PLAYER_ID", "GAME_ID", "TEAM_ID", "PTS", "AST", "REB", "BLK", "FGA", "FGM", "FTA", "FTM"
            ]].copy()
            selected.columns = [
                "player_id", "game_id", "team_id", "points", "assists", "rebounds", "blocks",
                "FGA", "FGM", "FTA", "FTM"
            ]

            # Convert game_id to int and filter player and game IDs
            selected["game_id"] = selected["game_id"].astype(int)
            selected = selected[
                selected["player_id"].isin(valid_player_ids) &
                selected["game_id"].isin(valid_game_ids)
            ]

            # Append to CSV
            selected.to_csv(output_file, mode='a', index=False, header=not initialized)
            initialized = True

            print(f"[{idx}/{len(game_ids)}] Appended stats for game {game_id}")
            time.sleep(delay)

        except Exception as e:
            print(f"[{idx}/{len(game_ids)}] Failed for game {game_id}: {e}")

    print(f"All box scores saved incrementally to {output_file}")

if __name__ == "__main__":
    fetch_boxscores()
