from nba_api.stats.endpoints import playercareerstats

player_id = 201939  # Example: Stephen Curry

df = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
print(df.columns)
print(df.head(10))
