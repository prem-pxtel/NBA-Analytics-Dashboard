# NBA Analytics Dashboard

## 1. Project Overview

This is a full-stack web application dashboard that allows users to view NBA player and team statistics.

Users can sign up and safely authenticate (with password hashes stored in the backend).
<img width="550" height="310" alt="image" src="https://github.com/user-attachments/assets/1d796943-5846-4886-910f-a10736e3dfc3" />

Homepage:
<img width="1895" height="884" alt="image" src="https://github.com/user-attachments/assets/34814249-c2a1-4200-abe1-aa0f444091d1" />

E/R diagram showing the core relational schema:
<img width="1012" height="824" alt="image" src="https://github.com/user-attachments/assets/2be60c36-e348-49d5-9034-e2769069ed58" />
<img width="359" height="246" alt="image" src="https://github.com/user-attachments/assets/831f55c7-2b7d-49d7-8301-3ffe56864383" />


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
We can start using the application now, using NBA production data! If a manual data update is desired, we can proceed with step 4 below.

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



