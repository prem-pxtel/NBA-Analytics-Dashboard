from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd
import time

def save_games(last_n_seasons=5):
    all_games = []
    current_season = 2024
    for i in range(last_n_seasons):
        season = f"{current_season - i}-{str(current_season - i + 1)[-2:]}"
        print(f"Fetching season {season}")
        try:
            finder = leaguegamefinder.LeagueGameFinder(season_nullable=season)
            df = finder.get_data_frames()[0]
            all_games.append(df)
            time.sleep(0.7)
        except Exception as e:
            print(f"Failed to fetch season {season}: {e}")

    df = pd.concat(all_games, ignore_index=True)

    # Separate into home and away games
    home_games = df[df["MATCHUP"].str.contains("vs.")]
    away_games = df[df["MATCHUP"].str.contains("@")]

    home_games = home_games[["GAME_ID", "SEASON_ID", "GAME_DATE", "TEAM_ID", "PTS"]]
    away_games = away_games[["GAME_ID", "TEAM_ID", "PTS"]]

    home_games = home_games.rename(columns={"TEAM_ID": "home_team_id", "PTS": "home_score"})
    away_games = away_games.rename(columns={"TEAM_ID": "away_team_id", "PTS": "away_score"})

    games_df = pd.merge(home_games, away_games, on="GAME_ID")
    games_df = games_df[["GAME_ID", "SEASON_ID", "GAME_DATE", "home_team_id", "away_team_id", "home_score", "away_score"]]

    games_df.to_csv("data/games.csv", index=False)
    print("✅ Saved games.csv with full scores.")

if __name__ == "__main__":
    save_games()
