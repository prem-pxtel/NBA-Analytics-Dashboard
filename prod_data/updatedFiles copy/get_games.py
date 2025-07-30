import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder

def fetch_game_csv(season="2024-25", season_type="Regular Season", output_file="../data/games.csv", team_file="../data/teams.csv"):
    print("Fetching NBA games...")

    # Load valid team IDs
    valid_team_ids = set(pd.read_csv(team_file)["team_id"].unique())

    # Get all games
    gamefinder = leaguegamefinder.LeagueGameFinder(
        season_nullable=season,
        season_type_nullable=season_type
    )
    games_df = gamefinder.get_data_frames()[0]

    keep_cols = ["GAME_ID", "SEASON_ID", "GAME_DATE", "TEAM_ID", "MATCHUP", "PTS"]
    games_df = games_df[keep_cols]

    # Convert GAME_ID to int (removes leading zeros)
    games_df = games_df[games_df["GAME_ID"].notnull()]
    games_df["GAME_ID"] = games_df["GAME_ID"].astype(int)

    # Separate home and away teams using MATCHUP column
    home_games = games_df[games_df["MATCHUP"].str.contains("vs.", na=False)]
    away_games = games_df[games_df["MATCHUP"].str.contains("@", na=False)]

    # Merge home and away info by GAME_ID
    merged = pd.merge(
        home_games,
        away_games,
        on="GAME_ID",
        suffixes=("_home", "_away")
    )

    # Build game metadata table
    output = pd.DataFrame({
        "GAME_ID": merged["GAME_ID"],  # already int
        "SEASON_ID": merged["SEASON_ID_home"].astype(str).str[-4:].astype(int) + 1,
        "GAME_DATE": merged["GAME_DATE_home"],
        "home_team_id": merged["TEAM_ID_home"],
        "away_team_id": merged["TEAM_ID_away"],
        "home_score": merged["PTS_home"],
        "away_score": merged["PTS_away"],
    })

    # Filter out games with invalid home or away team IDs
    output = output[
        output["home_team_id"].isin(valid_team_ids) &
        output["away_team_id"].isin(valid_team_ids)
    ]

    output = output.drop_duplicates(subset=["GAME_ID"])
    output.to_csv(output_file, index=False)
    print(f"Saved game metadata to {output_file}")

if __name__ == "__main__":
    fetch_game_csv()
