import csv
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
import time

def fetch_active_players_to_csv(filename="player.csv"):
    active_players = players.get_active_players()
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "player_id", "player_name", "birth_date", "position",
            "is_active", "weight", "height", "draft_year"
        ])
        
        for player in active_players:
            player_id = player['id']
            player_name = player['full_name']

            try:
                info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                data = info.get_normalized_dict()['CommonPlayerInfo'][0]
                
                birth_date = data.get("BIRTHDATE", "")[:10] if data.get("BIRTHDATE") else ""
                position = data.get("POSITION", "")
                is_active = data.get("ROSTERSTATUS") == 1
                weight = data.get("WEIGHT", "")
                height = data.get("HEIGHT", "")
                draft_year = data.get("DRAFT_YEAR", "")
                
                # Convert height to inches
                if height and '-' in height:
                    feet, inches = map(int, height.split('-'))
                    height_inches = round(feet * 12 + inches, 1)
                else:
                    height_inches = ""

                weight = float(weight) if weight else ""
                draft_year = float(draft_year) if draft_year and draft_year != 'Undrafted' else ""

                writer.writerow([
                    player_id, player_name, birth_date, position,
                    is_active, weight, height_inches, draft_year
                ])
                time.sleep(0.5)  
            except Exception as e:
                print(f"Error fetching data for {player_name} ({player_id}): {e}")
                continue

fetch_active_players_to_csv()
