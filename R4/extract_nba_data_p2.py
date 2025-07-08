# 02_fetch_game_and_stats.py

import os
import time
import random
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog, playercareerstats
from requests.exceptions import RequestException

os.makedirs("data", exist_ok=True)

def append_to_csv(df, filepath):
    if os.path.exists(filepath):
        df.to_csv(filepath, mode='a', index=False, header=False)
    else:
        df.to_csv(filepath, mode='w', index=False, header=True)

def get_team_logs_with_retry(team_id, season, max_retries=3):
    for attempt in range(max_retries):
        try:
            return teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed for team_id {team_id}: {e}")
            time.sleep(3)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)
    print(f"Failed for team_id {team_id}")
    return None

def save_games(season, season_id, team_list, seen_games):
    all_games = []
    for team in team_list:
        logs = get_team_logs_with_retry(team["id"], season)
        if logs is None:
            continue
        for _, row in logs.iterrows():
            game_id = int(row["Game_ID"])
            if game_id in seen_games:
                continue
            seen_games.add(game_id)

            is_home = "vs." in row["MATCHUP"]
            opp_abbr = row["MATCHUP"].split(" ")[-1]
            opp_team_id = next((t["id"] for t in team_list if t["abbreviation"] == opp_abbr), None)

            home_team_id = team["id"] if is_home else opp_team_id
            away_team_id = opp_team_id if is_home else team["id"]
            home_score = int(row["PTS"]) if is_home else None
            away_score = int(row["PTS"]) if not is_home else None

            all_games.append({
                "game_id": game_id,
                "season_id": season_id,
                "game_date": pd.to_datetime(row["GAME_DATE"]),
                "home_team_id": home_team_id,
                "away_team_id": away_team_id,
                "home_score": home_score,
                "away_score": away_score
            })
        time.sleep(1.5)

    append_to_csv(pd.DataFrame(all_games), "data/games.csv")
    print(f"Saved {len(all_games)} games for {season}")

def save_random_player_game_stats(players_df, games_df):
    stats = []
    sampled_games = games_df.sample(min(100, len(games_df)))
    sampled_players = players_df.sample(min(100, len(players_df)))

    for _, game in sampled_games.iterrows():
        for _, player in sampled_players.iterrows():
            stats.append({
                "player_id": player["player_id"],
                "game_id": game["game_id"],
                "team_id": game["home_team_id"],
                "points": random.randint(0, 40),
                "assists": random.randint(0, 10),
                "rebounds": random.randint(0, 15),
                "blocks": random.randint(0, 5),
                "FGA": random.randint(1, 20),
                "FGM": random.randint(0, 15),
                "FTA": random.randint(0, 10),
                "FTM": random.randint(0, 10)
            })
    append_to_csv(pd.DataFrame(stats), "data/boxscores.csv")
    print("Saved boxscores.csv")

def save_random_shots(players_df, games_df):
    shots = []
    shot_id_counter = 1
    for _, game in games_df.sample(min(50, len(games_df))).iterrows():
        for _, player in players_df.sample(min(10, len(players_df))).iterrows():
            for _ in range(random.randint(1, 5)):
                shots.append({
                    "shot_id": shot_id_counter,
                    "player_id": player["player_id"],
                    "game_id": game["game_id"],
                    "shot_type": random.choice(["2PT", "3PT", "FT"]),
                    "result": random.choice(["made", "missed"]),
                    "minutes_remaining": random.randint(0, 11),
                    "seconds_remaining": random.randint(0, 59)
                })
                shot_id_counter += 1
    append_to_csv(pd.DataFrame(shots), "data/shot.csv")
    print("Saved shot.csv")

def save_recent_player_seasons(players_df, max_seasons=5):
    all_stats = []
    for _, player in players_df.iterrows():
        try:
            df = playercareerstats.PlayerCareerStats(player_id=player["player_id"]).get_data_frames()[0]
            df = df[df["LEAGUE_ID"] == "00"]
            df = df[df["SEASON_TYPE"] == "Regular Season"]
            df = df.sort_values("SEASON_ID", ascending=False).head(max_seasons)
            df["player_id"] = player["player_id"]
            df["player_name"] = player["player_name"]
            all_stats.append(df)
        except:
            continue
        time.sleep(0.5)

    if all_stats:
        combined = pd.concat(all_stats)
        combined.to_csv("data/current_player_seasons.csv", index=False)
        print("Saved current_player_seasons.csv")

if __name__ == "__main__":
    last_5_seasons = ["2023-24", "2022-23", "2021-22", "2020-21", "2019-20"]
    season_map = {"2023-24": 2024, "2022-23": 2023, "2021-22": 2022, "2020-21": 2021, "2019-20": 2020}
    team_list = teams.get_teams()
    seen_games = set()

    for season in last_5_seasons:
        season_id = season_map[season]
        save_games(season, season_id, team_list, seen_games)

    players_df = pd.read_csv("data/players.csv")
    games_df = pd.read_csv("data/games.csv")

    save_random_player_game_stats(players_df, games_df)
    save_random_shots(players_df, games_df)
    save_recent_player_seasons(players_df)
