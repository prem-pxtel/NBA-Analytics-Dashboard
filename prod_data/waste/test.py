import csv

input_file = "data/player_season_stats.csv"
output_file = "player_season_stats_deduped.csv"

# Track seen (player_id, season_id) pairs
seen = set()

with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        key = (row["player_id"], row["season_id"])
        if key not in seen:
            writer.writerow(row)
            seen.add(key)

print(f"Duplicates removed. Cleaned file saved to: {output_file}")
