# CS348 Group Project – NBA Dashboard

## 1. Project Overview

This project is an NBA dashboard web application that allows users to view player and team statistics.  
For this milestone, we are using a simple dataset to demonstrate database setup and a basic query.

---

## 2. Prerequisites

You will need the following installed:

- Python 3.x (with Flask and Flask-CORS)
- PostgreSQL v14+
- Git (to clone the repository)
- NPM to install React

---

## 3. Setting Up the Sample Database

Make yourself a psql database with the information in .env and give yourself superuser

### Clone the Repository
```bash
git clone https://github.com/saileshp56/CS348-Group-Project.git
cd CS348-Group-Project
```
### Terminal 1:
```bash
cd frontend/
npm start
```
### Terminal 2:
```bash
cd backend/
python3 main.py
```
We can stop here, and start using the application now! If a manual data update is desired first, we can proceed with step 4 below.

## 4. Populating the Production Database
We use the following API package as the source of our production data: https://github.com/swar/nba_api

We use this package to scrape the raw data, using python scripts developed in this milestone:
- get_seasons.py
- get_teams.py
- get_games.py
- active_players.py
- boxscores.py
- player_season.py
- player_team.py

These should be run once, in the order as shown above (if the data has not already been generated), with some time in between to prevent rate limiting. 

Once the data is generated, all we need to do is run create_tables.sql followed by load_csv.sql. This will get the production data populated into our database, in case a refresh is necessary. 



