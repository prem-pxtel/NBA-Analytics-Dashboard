--- ========== TABLES ==========

DROP TABLE IF EXISTS Player CASCADE;
DROP TABLE IF EXISTS Team CASCADE;
DROP TABLE IF EXISTS Season CASCADE;
DROP TABLE IF EXISTS Game CASCADE;
DROP TABLE IF EXISTS PlayerGameStats CASCADE;
DROP TABLE IF EXISTS PlayerSeasonStats CASCADE;
DROP TABLE IF EXISTS PlayerTeamHistory CASCADE;
DROP TABLE IF EXISTS PlayerStatsAudit CASCADE;

-- Player table
CREATE TABLE Player (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100),
    birth_date DATE,
    position VARCHAR(30),
    is_active BOOLEAN,
    weight FLOAT,
    height FLOAT,
    draft_year FLOAT
);

CREATE INDEX idx_player_name ON Player(player_name);

-- Team table
CREATE TABLE Team (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(100),
    city VARCHAR(100),
    abbreviation VARCHAR(10)
);

-- Season table
CREATE TABLE Season (
    season_id INT PRIMARY KEY,
    season_type VARCHAR(20),
    season_start_date DATE,
    season_end_date DATE
);

-- Game table 
CREATE TABLE Game (
    game_id INT PRIMARY KEY,
    season_id INT,
    game_date DATE,
    home_team_id INT,
    away_team_id INT,
    home_score INT,
    away_score INT,
    FOREIGN KEY (season_id) REFERENCES Season(season_id),
    FOREIGN KEY (home_team_id) REFERENCES Team(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Team(team_id)
);

-- PlayerGameStats table
CREATE TABLE PlayerGameStats (
    player_id INT,
    game_id INT,
    team_id INT,
    points FLOAT,
    assists FLOAT,
    rebounds FLOAT,
    blocks FLOAT,
    FGA FLOAT,
    FGM FLOAT,
    FTA FLOAT,
    FTM FLOAT,
    PRIMARY KEY (player_id, game_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);

-- PlayerSeasonStats table (now using season_id)
CREATE TABLE PlayerSeasonStats (
    player_id INT,
    team_id INT,
    season_id INT,
    points_per_game FLOAT,
    assists_per_game FLOAT,
    rebounds_per_game FLOAT,
    blocks_per_game FLOAT,
    PRIMARY KEY (player_id, season_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id),
    FOREIGN KEY (season_id) REFERENCES Season(season_id)
);

-- PlayerTeamHistory table
CREATE TABLE PlayerTeamHistory (
    player_id INT,
    team_id INT,
    start_season INT,
    end_season INT,
    PRIMARY KEY (player_id, start_season, team_id),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);


--- PlayerStatsAudit table
CREATE TABLE PlayerStatsAudit (
    update_id SERIAL PRIMARY KEY,
    update_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    player_id INT NOT NULL,
    game_id INT,
    team_id INT,
    points FLOAT,
    assists FLOAT,
    rebounds FLOAT,
    blocks FLOAT,
    FGA FLOAT,
    FGM FLOAT,
    FTA FLOAT,
    FTM FLOAT
);


--- ========== VIEWS ========== 

CREATE MATERIALIZED VIEW PlayerSeasonStatsMV AS
SELECT
    p.player_name,
    ps.player_id,
    ps.team_id,
    ps.season_id,
    SUM(ps.points_per_game) AS total_points,
    AVG(ps.assists_per_game) AS avg_assists,
    AVG(ps.rebounds_per_game) AS avg_rebounds,
    AVG(ps.blocks_per_game) AS avg_blocks
FROM
    PlayerSeasonStats ps JOIN Player p ON ps.player_id = p.player_id
GROUP BY
    ps.player_id, ps.team_id, ps.season_id, p.player_id;


DROP VIEW IF EXISTS MostRecentGame;

CREATE VIEW MostRecentGame AS
SELECT
    p.player_id,
    p.player_name,
    g.game_date,
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
WHERE (pg.player_id, g.game_date) IN (
    SELECT player_id, MAX(game_date)
    FROM PlayerGameStats pg2
    JOIN Game g2 ON pg2.game_id = g2.game_id
    GROUP BY player_id
);


--- ========== TRIGGERS ==========
DROP FUNCTION IF EXISTS AuditPlayerGameStatsUpdate() CASCADE;


CREATE FUNCTION AuditPlayerGameStatsUpdate()
    RETURNS trigger AS $$
    BEGIN
        INSERT INTO PlayerStatsAudit (
            update_time,
            player_id,
            game_id,
            team_id,
            points,
            assists,
            rebounds,
            blocks,
            FGA,
            FGM,
            FTA,
            FTM
        )
        VALUES (
            NOW(),
            OLD.player_id,
            OLD.game_id,
            OLD.team_id,
            OLD.points,
            OLD.assists,
            OLD.rebounds,
            OLD.blocks,
            OLD.FGA,
            OLD.FGM,
            OLD.FTA,
            OLD.FTM
        );
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;


CREATE TRIGGER TriggerPlayerGameStatsUpdate
    AFTER UPDATE ON PlayerGameStats
    REFERENCING OLD TABLE AS old_table
    FOR EACH ROW
    EXECUTE FUNCTION AuditPlayerGameStatsUpdate();
