import pandas as pd

# Load both CSVs
boxscores_df = pd.read_csv("data/boxscores.csv")
games_df = pd.read_csv("data/games.csv")

# Get valid game IDs from games.csv
valid_game_ids = set(games_df["GAME_ID"].astype(str).unique())

# Keep only rows in boxscores.csv where game_id is valid
filtered_boxscores_df = boxscores_df[boxscores_df["game_id"].astype(str).isin(valid_game_ids)]

# Save the cleaned data
filtered_boxscores_df.to_csv("boxscores_filtered.csv", index=False)

print("Filtered boxscores saved to boxscores_filtered.csv.")
