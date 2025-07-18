CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY, -- SERIAL assigns sequential values automatically
    username VARCHAR(50) UNIQUE NOT NULL,
    pwd_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'viewer' -- 'admin' or 'viewer'
);

CREATE UNIQUE INDEX idx_username ON "User" (username);
