# extract_nba_data.py

from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonallplayers, teamgamelog, boxscoretraditionalv2
import pandas as pd
import os
import time

# Create output folder 
os.makedirs("data", exist_ok=True)

# TEAMS 
def save_teams():
    all_teams = teams.get_teams()
    df_teams = pd.DataFrame(all_teams)
    df_teams.to_csv("data/teams.csv", index=False)
    print("Saved data/teams.csv")

# PLAYERS 
def save_players():
    df_players = commonallplayers.CommonAllPlayers(is_only_current_season=0).get_data_frames()[0]
    df_players.to_csv("data/players.csv", index=False)
    print("Saved data/players.csv")

# GAMES 
def save_team_game_logs(season="2023-24"):
    team_list = teams.get_teams()
    all_logs = []

    for team in team_list:
        team_id = team['id']
        try:
            log_df = teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
            log_df['TEAM_ID'] = team_id
            all_logs.append(log_df)
            print(f"Fetched logs for {team['full_name']}")
            time.sleep(1.2)
        except Exception as e:
            print(f"Failed to fetch logs for {team['full_name']}: {e}")

    if all_logs:
        pd.concat(all_logs, ignore_index=True).to_csv("data/games.csv", index=False)
        print("Saved data/games.csv")

# BOX SCORES
def get_box_scores(game_ids, max_games=20, output_file="data/boxscores.csv"):
    boxscore_rows = []

    for i, gid in enumerate(game_ids[:max_games]):
        try:
            print(f"Fetching box score {i+1}/{max_games} for game_id: {gid}")
            box_df = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gid).get_data_frames()[0]
            box_df["GAME_ID"] = gid
            boxscore_rows.append(box_df)
            time.sleep(1.5)
        except Exception as e:
            print(f"Failed for game_id {gid}: {e}")

    if boxscore_rows:
        full_df = pd.concat(boxscore_rows, ignore_index=True)
        full_df.to_csv(output_file, index=False)
        print(f"Saved box scores to {output_file}")
    else:
        print("! No box scores were fetched.")


# MAIN 
if __name__ == "__main__":
    save_teams()
    save_players()
    save_team_game_logs(season="2023-24")

    try:
        games_df = pd.read_csv("data/games.csv")
        if "Game_ID" in games_df.columns:
            game_ids = games_df["Game_ID"].astype(str).str.zfill(10).unique()
            print(f"Found {len(game_ids)} unique game IDs. Example: {game_ids[:3]}")
            get_box_scores(game_ids, max_games=20)
        else:
            print("! 'Game_ID' column not found in games.csv")
    except Exception as e:
        print(f"! Could not load games.csv for box scores: {e}")
