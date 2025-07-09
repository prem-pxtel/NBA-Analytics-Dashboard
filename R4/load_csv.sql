\COPY Player FROM 'data/players.csv' DELIMITER ',' CSV HEADER;
\COPY Team FROM 'data/teams.csv' DELIMITER ',' CSV HEADER;
\COPY Season FROM 'data/seasons.csv' DELIMITER ',' CSV HEADER;
\COPY PlayerTeamHistory FROM 'data/player_team_history.csv' DELIMITER ',' CSV HEADER;
\COPY playergamestats(player_id, game_id, team_id, points, assists, rebounds, blocks, fga, fgm, fta, ftm) FROM 'data/boxscores.csv' CSV HEADER;