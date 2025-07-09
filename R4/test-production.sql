-- Top 5 scorers
SELECT player_id, SUM(points) AS total_points
FROM playergamestats
GROUP BY player_id
ORDER BY total_points DESC
FETCH FIRST 5 ROWS ONLY;

-- Average total points per game
SELECT AVG(home_score + away_score) AS avg_total_pts
FROM game
WHERE home_score IS NOT NULL AND away_score IS NOT NULL;

-- Games won by 'Los Angeles Lakers' (team_id = 1610612747)
SELECT g.*
FROM game g
WHERE 
    (g.home_team_id = 1610612747 AND g.home_score > g.away_score)
    OR
    (g.away_team_id = 1610612747 AND g.away_score > g.home_score);
