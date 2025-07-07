-- Load Teams
\COPY Teams(id, full_name, abbreviation, nickname, city, state, year_founded)
FROM 'data/teams.csv' DELIMITER ',' CSV HEADER;

-- Load Players
\COPY Players(person_id, display_first_last, rosterstatus, from_year, to_year, team_id)
FROM 'data/players.csv' DELIMITER ',' CSV HEADER;

-- Load Games
\COPY Games(game_id, game_date, matchup, wl, w, l, w_pct, min, fgm, fga, fg_pct,
            fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast,
            stl, blk, tov, pf, pts, team_id)
FROM 'data/games.csv' DELIMITER ',' CSV HEADER;

-- Load PlayerGameStats
\COPY PlayerGameStats(game_id, team_id, player_id, player_name, start_position, min, fgm,
                      fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb,
                      ast, stl, blk, tov, pf, pts)
FROM 'data/boxscores.csv' DELIMITER ',' CSV HEADER;
