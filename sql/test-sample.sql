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
WHERE ps.player_id = {player_id}
    AND s.season_id = {season_id};
-- R7: Player Stats Per Game
-- individual game performance for a given player and game
SELECT p.player_name,
    g.game_date,
    home.team_name AS home_team,
    away.team_name AS away_team,
    pg.points,
    pg.assists,
    pg.rebounds,
    pg.blocks
FROM PlayerGameStats pg
    JOIN Game g ON pg.game_id = g.game_id
    JOIN Team home ON g.home_team_id = home.team_id
    JOIN Team away ON g.away_team_id = away.team_id
    JOIN Player p ON pg.player_id = p.player_id
WHERE pg.player_id = {player_id}
    AND g.game_id = {game_id};
-- R8: Player's Best Game by Stat
-- best game where given player performed best in given category
SELECT p.player_name,
    g.game_date,
    home.team_name AS home_team,
    away.team_name AS away_team,
    pg.points,
    pg.assists,
    pg.rebounds,
    pg.blocks
FROM PlayerGameStats pg
    JOIN Game g ON pg.game_id = g.game_id
    JOIN Team home ON g.home_team_id = home.team_id
    JOIN Team away ON g.away_team_id = away.team_id
    JOIN Player p ON pg.player_id = p.player_id
WHERE pg.player_id = {player_id}
ORDER BY pg.{stat} DESC
LIMIT 1;
-- R9: Top 10 All-Time Scorers
-- 10 players with highest career points
SELECT p.player_name,
    SUM(pg.points) AS total_points
FROM Player p
    JOIN PlayerGameStats pg ON p.player_id = pg.player_id
GROUP BY p.player_id,
    p.player_name
ORDER BY total_points DESC
LIMIT 10;