-- Insert Season
INSERT INTO Season VALUES
(2022, 'Regular', '2022-10-01', '2023-04-15');

-- Insert Teams
INSERT INTO Team VALUES
(1, 'Los Angeles Lakers', 'Los Angeles', 'LAL'),
(2, 'Golden State Warriors', 'San Francisco', 'GSW'),
(3, 'Milwaukee Bucks', 'Milwaukee', 'MIL');

-- Insert Players (order corrected to match schema)
INSERT INTO Player VALUES
(1, 'LeBron James', '1984-12-30', 'SF', TRUE, 250, 81, 2003),
(2, 'Stephen Curry', '1988-03-14', 'PG', TRUE, 185, 74, 2009),
(3, 'Giannis Antetokounmpo', '1994-12-06', 'PF', TRUE, 242, 83, 2013),
(4, 'Kobe Bryant', '1978-08-23', 'SG', FALSE, 212, 78, 1996),
(5, 'Kevin Durant', '1988-09-29', 'SF', TRUE, 240, 82, 2007);

-- Insert Games
INSERT INTO Game VALUES
(1, 2022, '2022-10-20', 1, 2, 102, 99),
(2, 2022, '2022-11-01', 3, 1, 120, 110);

-- Insert Shots
INSERT INTO Shot VALUES
(1, 1, 1, '3PT', 'Made', 2, 15),
(2, 2, 1, '2PT', 'Missed', 4, 10),
(3, 3, 2, '3PT', 'Made', 3, 45),
(4, 1, 2, '2PT', 'Made', 5, 20);

-- Insert PlayerGameStats (includes team_id)
INSERT INTO PlayerGameStats VALUES
(1, 1, 1, 29, 7, 8, 1, 22, 10, 5, 4),
(2, 1, 2, 31, 9, 6, 0, 18, 12, 3, 3),
(3, 2, 3, 34, 5, 14, 2, 24, 15, 6, 5);

-- Insert PlayerSeasonStats (uses season_id as INT and includes team_id)
INSERT INTO PlayerSeasonStats VALUES
(1, 1, 2022, 8.3, 27.5, 1.1, 7.1),
(2, 2, 2022, 6.5, 25.3, 0.4, 5.2),
(3, 3, 2022, 5.9, 29.9, 1.3, 11.4);

-- Insert PlayerTeamHistory (start/end season as INTs)
INSERT INTO PlayerTeamHistory VALUES
(1, 1, 2003, 2023),
(2, 2, 2009, 2023),
(3, 3, 2013, 2023),
(4, 1, 1996, 2016),
(5, 2, 2007, 2016);
