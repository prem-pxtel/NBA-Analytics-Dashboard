INSERT INTO Player VALUES
(1, 'LeBron James', '1984-12-30', 250, 81, 'SF', 2003, TRUE),
(2, 'Stephen Curry', '1988-03-14', 185, 75, 'PG', 2009, TRUE),
(3, 'Kevin Durant', '1988-09-29', 240, 82, 'SF', 2007, TRUE),
(4, 'Giannis Antetokounmpo', '1994-12-06', 242, 83, 'PF', 2013, TRUE),
(5, 'Jayson Tatum', '1998-03-03', 210, 80, 'SF', 2017, TRUE);

INSERT INTO Team VALUES
(1, 'Los Angeles Lakers', 'Los Angeles', 'LAL'),
(2, 'Golden State Warriors', 'San Francisco', 'GSW'),
(3, 'Boston Celtics', 'Boston', 'BOS');

INSERT INTO Game VALUES
(1, '2022', '2022-12-15', 1, 2, 110, 105),
(2, '2022', '2022-12-20', 3, 1, 102, 108);

INSERT INTO PlayerSeasonStats VALUES
(1, '2022', 27.5, 8.3, 7.1, 1.1),
(2, '2022', 30.1, 6.5, 5.2, 0.4),
(3, '2022', 28.2, 5.6, 6.0, 1.2),
(4, '2022', 29.5, 5.9, 11.0, 1.3),
(5, '2022', 26.4, 4.4, 7.1, 0.6);

INSERT INTO PlayerGameStats VALUES
(1, 1, 29, 7, 8, 1, 22, 10, 5, 4),
(2, 1, 31, 6, 5, 0, 20, 11, 6, 6),
(3, 1, 27, 5, 6, 2, 18, 9, 4, 3),
(4, 2, 34, 4, 12, 3, 24, 13, 9, 6),
(5, 2, 28, 5, 7, 1, 21, 10, 5, 5);

INSERT INTO PlayerTeamHistory VALUES
(1, 1, '2003', '2025'),
(2, 2, '2009', '2025'),
(3, 2, '2007', '2025'),
(4, 3, '2013', '2025'),
(5, 3, '2017', '2025');

INSERT INTO Shot VALUES
(1, 1, 1, '3PT', 'Made', 5, 32),
(2, 1, 1, '2PT', 'Missed', 2, 18),
(3, 2, 1, '3PT', 'Made', 1, 44),
(4, 2, 1, '2PT', 'Missed', 0, 22),
(5, 3, 1, '3PT', 'Made', 3, 15),
(6, 4, 2, '2PT', 'Made', 4, 33),
(7, 4, 2, '3PT', 'Missed', 2, 21),
(8, 5, 2, '2PT', 'Made', 1, 14),
(9, 5, 2, '3PT', 'Made', 0, 5);

