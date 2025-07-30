import csv
from nba_api.stats.static import teams

def fetch_teams_to_csv(filename="../data/teams.csv"):
    all_teams = teams.get_teams()

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["team_id", "team_name", "city", "abbreviation"])

        for team in all_teams:
            team_id = team.get("id", "")
            team_name = team.get("full_name", "")
            city = team.get("city", "")
            abbreviation = team.get("abbreviation", "")

            writer.writerow([team_id, team_name, city, abbreviation])

fetch_teams_to_csv()
