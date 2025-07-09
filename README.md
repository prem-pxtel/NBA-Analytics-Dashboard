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

## 4. Populating the Production Database
We use the following API package as the source of our production data: https://github.com/swar/nba_api

We use this package to scrape the raw data, using python scripts developed in this milestone:
- extract_nba_data_p1.py
- extract_nba_data_p2.py
- player_team.py
- boxscores.py

These should be run once, in the order as shown above (if the data has not already been generated), with some time in between to prevent rate limiting. 

Once the data is generated, all we need to do is run create_tables.sql followed by load_csv.sql. This will get the production data populated into our database.

Currently in our frontend, we are creating tables and loading in sample data as shown below.

```sql
 # In main.py...
 # ...
 try:
	 run_sql_file(cursor, db, "sql/create_tables.sql")
	 print("Created tables")
	 run_sql_file(cursor, db, "sql/sample_data.sql")
	 print("Loaded sample data")
 # ...
```

Currently, we are using the sample dataset for comparison with expected output in our report. However, to use the production data instead, we need to simply run load_csv.sql here.



