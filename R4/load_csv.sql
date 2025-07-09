-- Load Player data
\COPY Player FROM 'data/players.csv' DELIMITER ',' CSV HEADER;

-- Load Team data
\COPY Team FROM 'data/teams.csv' DELIMITER ',' CSV HEADER;

-- Load Season data
\COPY Season FROM 'data/seasons.csv' DELIMITER ',' CSV HEADER;

-- Load PlayerTeamHistory data
\COPY PlayerTeamHistory FROM 'data/player_team_history.csv' DELIMITER ',' CSV HEADER;

-- Load Game data
\COPY Game FROM 'data/games.csv' DELIMITER ',' CSV HEADER;

-- Load PlayerGameStats data
\COPY PlayerGameStats(player_id, game_id, team_id, points, assists, rebounds, blocks, fga, fgm, fta, ftm) FROM 'data/boxscores.csv' DELIMITER ',' CSV HEADER;

\COPY PlayerSeasonStats FROM 'data/player_season_stats.csv' DELIMITER ',' CSV HEADER;


