import csv
import time
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

def fetch_player_season_stats_avg(filename="../data/player_season_stats.csv"):
    all_players = players.get_active_players()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "player_id", "team_id", "season_id",
            "points_per_game", "assists_per_game", "rebounds_per_game", "blocks_per_game"
        ])

        # Set to track (player_id, season_id) already written
        written_seasons = set()

        for player in all_players:
            player_id = player["id"]

            try:
                career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
                data = career_stats.get_normalized_dict()["SeasonTotalsRegularSeason"]

                for season in data:
                    # Skip if any required data is missing
                    if not season.get("TEAM_ID") or not season.get("SEASON_ID"):
                        continue

                    games_played = int(season.get("GP", 0))
                    if games_played == 0:
                        continue

                    season_id = int(season["SEASON_ID"][:4]) + 1

                    # Skip if we've already written this player-season
                    if (player_id, season_id) in written_seasons:
                        continue

                    team_id = int(season["TEAM_ID"])
                    points_per_game = round(float(season.get("PTS", 0)) / games_played, 2)
                    assists_per_game = round(float(season.get("AST", 0)) / games_played, 2)
                    rebounds_per_game = round(float(season.get("REB", 0)) / games_played, 2)
                    blocks_per_game = round(float(season.get("BLK", 0)) / games_played, 2)

                    writer.writerow([
                        player_id, team_id, season_id,
                        points_per_game, assists_per_game, rebounds_per_game, blocks_per_game
                    ])

                    written_seasons.add((player_id, season_id))

                time.sleep(0.6) 
            except Exception as e:
                print(f"Error processing player ID {player_id}: {e}")
                continue

fetch_player_season_stats_avg()
