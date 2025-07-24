import csv

def write_seasons_to_csv(filename="seasons.csv"):
    seasons = []
    for end_year in range(2025, 2002, -1):  
        start_year = end_year - 1
        season = {
            "season_id": end_year,
            "season_type": "Regular Season",
            "season_start_date": f"{start_year}-10-01",
            "season_end_date": f"{end_year}-04-15"
        }
        seasons.append(season)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["season_id", "season_type", "season_start_date", "season_end_date"])
        for season in seasons:
            writer.writerow([
                season["season_id"],
                season["season_type"],
                season["season_start_date"],
                season["season_end_date"]
            ])

write_seasons_to_csv()
