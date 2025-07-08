# 01_fetch_static_data.py

import os
import time
import random
import pandas as pd
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import commonplayerinfo

os.makedirs("data", exist_ok=True)

def append_to_csv(df, filepath):
    if os.path.exists(filepath):
        df.to_csv(filepath, mode='a', index=False, header=False)
    else:
        df.to_csv(filepath, mode='w', index=False, header=True)

def to_inches(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return feet * 12 + inches
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
    append_to_csv(df, "data/teams.csv")
    print("Saved teams.csv")

def save_players():
    current_players = players.get_active_players()
    detailed_data = []

    for player in current_players:
        player_id = player["id"]
        player_name = player["full_name"]
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
            birth_date = info.at[0, "BIRTHDATE"][:10]
            position = info.at[0, "POSITION"]
            weight = int(info.at[0, "WEIGHT"])
            height = to_inches(info.at[0, "HEIGHT"])
            draft_year = info.at[0, "DRAFT_YEAR"]
            draft_year = None if draft_year == "Undrafted" else int(draft_year)
        except:
            birth_date, position, weight, height, draft_year = None, None, None, None, None

        detailed_data.append({
            "player_id": player_id,
            "player_name": player_name,
            "birth_date": birth_date,
            "position": position,
            "is_active": True,
            "weight": weight,
            "height": height,
            "draft_year": draft_year
        })
        time.sleep(0.5)

    df = pd.DataFrame(detailed_data)
    append_to_csv(df, "data/players.csv")
    print("Saved players.csv")
    return df

def save_seasons(season_map):
    rows = []
    for season_str, season_id in season_map.items():
        start_year = int(season_str.split("-")[0])
        end_year = int(season_str.split("-")[1]) + 2000
        rows.append({
            "season_id": season_id,
            "season_type": "Regular Season",
            "season_start_date": f"{start_year}-10-01",
            "season_end_date": f"{end_year}-04-15"
        })
    append_to_csv(pd.DataFrame(rows), "data/seasons.csv")
    print("Saved seasons.csv")

if __name__ == "__main__":
    save_teams()
    players_df = save_players()
    teams_df = pd.read_csv("data/teams.csv")

    season_map = {"2023-24": 2024, "2022-23": 2023, "2021-22": 2022, "2020-21": 2021, "2019-20": 2020}
    save_seasons(season_map)

    
