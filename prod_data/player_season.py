import csv

# File paths
players_file = "data/players.csv"
season_stats_file = "player_season_stats.csv"
output_file = "data/player_season_stats.csv"

# Load valid player_ids from players.csv
valid_player_ids = set()
with open(players_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        valid_player_ids.add(row["player_id"])

# Read and filter player_season_stats.csv
with open(season_stats_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        if row["player_id"] in valid_player_ids:
            writer.writerow(row)

print(f"✅ Filtered file written to {output_file}")
