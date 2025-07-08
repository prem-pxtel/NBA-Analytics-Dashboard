\COPY Player(player_id, player_name, birth_date, position, is_active, weight, height, draft_year) FROM 'data/players.csv' DELIMITER ',' CSV HEADER;

\COPY Team(team_id, team_name, city, abbreviation) FROM 'data/teams.csv' DELIMITER ',' CSV HEADER;

\COPY Season(season_id, season_type, season_start_date, season_end_date) FROM 'data/seasons.csv' DELIMITER ',' CSV HEADER;

\COPY Game(game_id, season_id, game_date, home_team_id, away_team_id, home_score, away_score) FROM 'data/games.csv' DELIMITER ',' CSV HEADER;

\COPY PlayerGameStats(player_id, game_id, team_id, points, assists, rebounds, blocks, FGA, FGM, FTA, FTM) FROM 'data/boxscores.csv' DELIMITER ',' CSV HEADER;
