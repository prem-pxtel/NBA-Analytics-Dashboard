-- Top 5 scorers
SELECT player_id, SUM(points) AS total_points
FROM PlayerGameStats
GROUP BY player_id
ORDER BY total_points DESC
FETCH FIRST 5 ROWS ONLY;

-- Average team points per game
SELECT team_id, AVG(pts) AS avg_pts
FROM Games
GROUP BY team_id;

-- Games won by 'Los Angeles Lakers'
SELECT *
FROM Games
WHERE matchup LIKE '%LAL%' AND wl = 'W';