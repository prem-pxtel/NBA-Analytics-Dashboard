-- R6: Player Stats Per Season
-- Retrieves per-season stats for a given player_id, ordered by season

SELECT
    p.player_name,
    s.season_year,
    t.team_name,
    ps.points_per_game,
    ps.assists_per_game,
    ps.rebounds_per_game,
    ps.blocks_per_game
FROM PlayerSeasonStats ps
    JOIN Season s ON ps.season_id = s.season_id
    JOIN Team t ON ps.team_id = t.team_id
    JOIN Player p ON ps.player_id = p.player_id
WHERE ps.player_id = %s
ORDER BY s.season_year;
