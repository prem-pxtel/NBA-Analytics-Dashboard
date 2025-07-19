DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    pwd_hash VARCHAR(255) NOT NULL,
    user_role VARCHAR(50) CHECK (user_role IN ('admin', 'viewer')) NOT NULL DEFAULT 'viewer' 
);

CREATE UNIQUE INDEX idx_username ON Users(username);
