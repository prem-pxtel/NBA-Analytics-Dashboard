import time
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder, boxscoretraditionalv2

def fetch_boxscores(season="2024-25", season_type="Regular Season", delay=0.6, output_file="boxscores.csv"):
    # Step 1: Get all games from the season
    print("Fetching game list...")
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable=season_type)
    games_df = gamefinder.get_data_frames()[0]
    game_ids = games_df['GAME_ID'].unique()

    print(f"Found {len(game_ids)} games. Downloading box scores...")

    # Step 2: Initialize output CSV with header from first valid game
    initialized = False

    for idx, game_id in enumerate(game_ids, 1):
        try:
            boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            stats_df = boxscore.player_stats.get_data_frame()

        # Filter out DNP players (where MIN is NaN or 0)
            stats_df = stats_df[stats_df["MIN"].notna() & (stats_df["MIN"] != "0")]

        # Select and rename columns to match your SQL table
            selected = stats_df[[
                "PLAYER_ID", "GAME_ID", "TEAM_ID", "PTS", "AST", "REB", "BLK", "FGA", "FGM", "FTA", "FTM"
            ]].copy()
            selected.columns = [
                "player_id", "game_id", "team_id", "points", "assists", "rebounds", "blocks",
                "FGA", "FGM", "FTA", "FTM"
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
