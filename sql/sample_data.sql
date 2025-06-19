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
(3, 3, 2022, 5.9, 29.9, 1.3, 11.4),
(1, 1, 2003, 20.9, 5.9, 5.5, 0.7),
(1, 1, 2004, 27.2, 7.2, 7.4, 0.7),
(1, 1, 2005, 31.4, 6.6, 7.0, 0.8),
(1, 1, 2006, 27.3, 6.0, 6.7, 0.7),
(1, 1, 2007, 30.0, 7.2, 7.9, 1.1),
(1, 1, 2008, 28.4, 7.2, 7.6, 1.1),
(1, 1, 2009, 29.7, 8.6, 7.3, 1.0),
(1, 1, 2010, 26.7, 7.0, 7.5, 0.6),
(1, 1, 2011, 27.1, 6.2, 7.9, 0.8),
(1, 1, 2012, 26.8, 7.3, 8.0, 0.9),
(1, 1, 2013, 27.1, 6.3, 6.9, 0.3),
(1, 1, 2014, 25.3, 7.4, 6.0, 0.7),
(1, 1, 2015, 25.3, 6.8, 7.4, 0.6),
(1, 1, 2016, 26.4, 8.7, 8.6, 0.6),
(1, 1, 2017, 27.5, 9.1, 8.6, 0.9),
(1, 1, 2018, 27.4, 8.3, 8.5, 0.6),
(1, 1, 2019, 25.3, 10.2, 7.8, 0.5),
(1, 1, 2020, 25.0, 7.8, 7.7, 0.6),
(1, 1, 2021, 30.3, 6.2, 8.2, 1.1),
(1, 1, 2022, 28.9, 6.8, 8.3, 0.5),
(1, 1, 2023, 25.7, 8.3, 7.3, 0.6);

-- Insert PlayerTeamHistory (start/end season as INTs)
INSERT INTO PlayerTeamHistory VALUES
(1, 1, 2003, 2023),
(2, 2, 2009, 2023),
(3, 3, 2013, 2023),
(4, 1, 1996, 2016),
(5, 2, 2007, 2016);
