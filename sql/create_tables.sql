-- Player table
CREATE TABLE Player (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100),
    position VARCHAR(10),
    is_active BOOLEAN,
    height INT,
    weight INT,
    draft_year INT,
    birth_date DATE
);
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
-- Shot table
CREATE TABLE Shot (
    shot_id INT PRIMARY KEY,
    player_id INT,
    game_id INT,
    shot_type VARCHAR(10),
    result VARCHAR(10),
    minutes_remaining INT,
    seconds_remaining INT,
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (game_id) REFERENCES Game(game_id)
);
-- PlayerGameStats table
CREATE TABLE PlayerGameStats (
    player_id INT,
    game_id INT,
    team_id INT,
    points INT,
    assists INT,
    rebounds INT,
    blocks INT,
    FGA INT,
    FGM INT,
    FTA INT,
    FTM INT,
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
    assists_per_game FLOAT,
    points_per_game FLOAT,
    blocks_per_game FLOAT,
    rebounds_per_game FLOAT,
    PRIMARY KEY (player_id, team_id, season_id),
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
    PRIMARY KEY (player_id, team_id, start_season),
    FOREIGN KEY (player_id) REFERENCES Player(player_id),
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
);