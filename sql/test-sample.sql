-- R6: Player Stats Per Season
-- Retrieves per-season stats for a given player_id and season
SELECT p.player_name,
    s.season_type,
    t.team_name,
    ps.points_per_game,
    ps.assists_per_game,
    ps.rebounds_per_game,
    ps.blocks_per_game
FROM PlayerSeasonStats ps
    JOIN Season s ON ps.season_id = s.season_id
    JOIN Team t ON ps.team_id = t.team_id
    JOIN Player p ON ps.player_id = p.player_id
WHERE p.player_name = 'LeBron James'
    AND s.season_id = 2022;

-- R7: Player Stats Per Game
-- individual game performance for a given player and game
SELECT 
    g.game_date AS date,
    CASE
        WHEN pg.team_id = g.home_team_id THEN away.team_name
        ELSE home.team_name
    END AS opponent,
    pg.points,
    pg.assists,
    pg.rebounds,
    pg.blocks
FROM PlayerGameStats pg
JOIN Player p ON pg.player_id = p.player_id
JOIN Game g ON pg.game_id = g.game_id
JOIN Team home ON g.home_team_id = home.team_id
JOIN Team away ON g.away_team_id = away.team_id
WHERE p.player_name = 'Stephen Curry';
    
-- R8: Player's Best Game by Stat
-- best game where given player performed best in given category
SELECT 
    g.game_date AS date,
    CASE
        WHEN pg.team_id = g.home_team_id THEN away.team_name
        ELSE home.team_name
    END AS opponent,
    pg.points,
    pg.assists,
    pg.rebounds,
    pg.blocks
FROM PlayerGameStats pg
JOIN Player p ON pg.player_id = p.player_id
JOIN Game g ON pg.game_id = g.game_id
JOIN Team home ON g.home_team_id = home.team_id
JOIN Team away ON g.away_team_id = away.team_id
WHERE p.player_name = 'Giannis Antetokounmpo'
ORDER BY pg.points DESC
LIMIT 1;

-- R9: Top 10 All-Time Scorers
-- 10 players with highest career points
SELECT 
    p.player_name,
    SUM(pg.points) AS total_points
FROM PlayerGameStats pg
JOIN Player p ON pg.player_id = p.player_id
GROUP BY p.player_name
ORDER BY total_points DESC
LIMIT 10;
