-- Load Teams
copy team FROM 'data/teams.csv' DELIMITER ',' CSV HEADER;

-- Load Players
copy player FROM 'data/players.csv' DELIMITER ',' CSV HEADER;

-- Load Games
copy game FROM 'data/games.csv' DELIMITER ',' CSV HEADER;

-- Load Player Game Stats (boxscores)
copy playergamestats (
    player_id, team_id, game_id, min, fgm, fga, fg_pct,
    fg3m, fg3a, fg3_pct, ftm, fta, ft_pct,
    oreb, dreb, reb, ast, stl, blk, tov, pf, pts
)
FROM 'data/boxscores.csv' DELIMITER ',' CSV HEADER;
