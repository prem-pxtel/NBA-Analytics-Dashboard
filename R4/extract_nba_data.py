# extract_nba_data.py

from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonallplayers, teamgamelog, boxscoretraditionalv2, commonplayerinfo
import pandas as pd
import os
import time

os.makedirs("data", exist_ok=True)

def convert_height_to_inches(height_str):
    try:
        feet, inches = height_str.split("-")
        return int(feet) * 12 + int(inches)
    except:
        return None

def save_teams():
    all_teams = teams.get_teams()
    df = pd.DataFrame(all_teams)
    df = df.rename(columns={
        "id": "team_id",
        "full_name": "team_name",
        "city": "city",
        "abbreviation": "abbreviation"
    })
    df = df[["team_id", "team_name", "city", "abbreviation"]]
    df.to_csv("data/teams.csv", index=False)
    print("Saved data/teams.csv")

def save_players():
    players = commonallplayers.CommonAllPlayers(is_only_current_season=1).get_data_frames()[0]
    players = players.rename(columns={
        "PERSON_ID": "player_id",
        "DISPLAY_FIRST_LAST": "player_name",
        "ROSTERSTATUS": "is_active"
    })
    detailed_data = []

    for i, row in players.iterrows():
        player_id = row["player_id"]
        player_name = row["player_name"]
        is_active = row["is_active"]
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
            birth_date_raw = info.at[0, "BIRTHDATE"]
            position = info.at[0, "POSITION"]
            weight = info.at[0, "WEIGHT"]
            height_raw = info.at[0, "HEIGHT"]
            draft_year_raw = info.at[0, "DRAFT_YEAR"]

            # Format birth_date as YYYY-MM-DD
            birth_date = pd.to_datetime(birth_date_raw).date()

            # Convert height "6-8" to inches
            if isinstance(height_raw, str) and '-' in height_raw:
                feet, inches = map(int, height_raw.split('-'))
                height = feet * 12 + inches
            else:
                height = None

            # Turns undrafted to NULL
            draft_year = None if draft_year_raw == "Undrafted" else draft_year_raw

        except Exception as e:
            birth_date, position, weight, height, draft_year = None, None, None, None, None

        detailed_data.append({
            "player_id": player_id,
            "player_name": player_name,
            "birth_date": birth_date,
            "position": position,
            "is_active": is_active,
            "weight": weight,
            "height": height,
            "draft_year": draft_year
        })

        time.sleep(0.6)

    df = pd.DataFrame(detailed_data)
    df.to_csv("data/players.csv", index=False)
    print("Saved data/players.csv")


def save_seasons():
    df = pd.DataFrame([{
        "season_id": 2024,
        "season_type": "Regular Season",
        "season_start_date": "2023-10-24",
        "season_end_date": "2024-04-14"
    }])
    df.to_csv("data/seasons.csv", index=False)
    print("Saved data/seasons.csv")

def save_games(season="2023-24"):
    all_games = []
    team_list = teams.get_teams()
    seen_games = set()

    for team in team_list:
        try:
            team_id = team["id"]
            logs = teamgamelog.TeamGameLog(team_id=team_id, season=season).get_data_frames()[0]
            for _, row in logs.iterrows():
                game_id = int(row["Game_ID"])
                if game_id in seen_games:
                    continue
                seen_games.add(game_id)

                is_home = "vs." in row["MATCHUP"]
                opp_abbr = row["MATCHUP"].split(" ")[-1]
                opp_team_id = next((t["id"] for t in team_list if t["abbreviation"] == opp_abbr), None)

                home_team_id = team_id if is_home else opp_team_id
                away_team_id = opp_team_id if is_home else team_id
                "home_score": int(row["PTS"]) if is_home else None
                "away_score": int(row["PTS"]) if not is_home else None


                all_games.append({
                    "game_id": game_id,
                    "season_id": 2024,
                    "game_date": pd.to_datetime(row["GAME_DATE"]),
                    "home_team_id": home_team_id,
                    "away_team_id": away_team_id,
                    "home_score": int(home_score) if home_score is not None else None,
                    "away_score": int(away_score) if away_score is not None else None
                })
            time.sleep(1.2)
        except Exception as e:
            print(f"Error with {team['full_name']}: {e}")

    df = pd.DataFrame(all_games)
    df.to_csv("data/games.csv", index=False)
    print("Saved data/games.csv")

def save_box_scores(game_ids, max_games=50, output_file="data/boxscores.csv"):
    stats_rows = []
    for i, gid in enumerate(game_ids[:max_games]):
        try:
            df = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gid).get_data_frames()[0]
            df = df.rename(columns={
                "PLAYER_ID": "player_id",
                "TEAM_ID": "team_id",
                "GAME_ID": "game_id",
                "PTS": "points",
                "AST": "assists",
                "REB": "rebounds",
                "BLK": "blocks",
                "FGA": "FGA",
                "FGM": "FGM",
                "FTA": "FTA",
                "FTM": "FTM"
            })
            df = df[["player_id", "game_id", "team_id", "points", "assists", "rebounds", "blocks", "FGA", "FGM", "FTA", "FTM"]]
            df = df.astype({
                "points": "Int64",
                "assists": "Int64",
                "rebounds": "Int64",
                "blocks": "Int64",
                "FGA": "Int64",
                "FGM": "Int64",
                "FTA": "Int64",
                "FTM": "Int64"
            })
            stats_rows.append(df)
            print(f"Fetched box score {i+1}/{max_games}")
            time.sleep(1.2)
        except Exception as e:
            print(f"Box score error for game {gid}: {e}")
    if stats_rows:
        pd.concat(stats_rows, ignore_index=True).to_csv(output_file, index=False)
        print(f"Saved cleaned box scores to {output_file}")

if __name__ == "__main__":
    save_teams()
    save_players()
    save_seasons()
    save_games(season="2023-24")

    try:
        games_df = pd.read_csv("data/games.csv")
        if "game_id" in games_df.columns:
            game_ids = games_df["game_id"].astype(str).str.zfill(10).unique()
            print(f"Found {len(game_ids)} game IDs")
            save_box_scores(game_ids, max_games=50)
        else:
            print("'game_id' not found in games.csv")
    except Exception as e:
        print(f"Could not load games.csv: {e}")
