import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PWD")
    )


def run_sql_file(cursor, db, path: str):
    with open(path, 'r') as sql_file:
        sql = sql_file.read()
        cursor.execute(sql)
        db.commit()


def load_query(path: str):
    with open(path, 'r') as file:
        sql = file.read()

    return [q.strip() for q in sql.split(';') if q.strip()]


def load_csv(cursor, db, table, csv_path):
    with open(csv_path, 'r') as f:
        cursor.copy_expert(f"COPY {table} FROM STDIN WITH CSV HEADER", f)
    db.commit()


def load_prod_data(cursor, db):
    load_csv(cursor, db, "Player", "prod_data/data/players.csv")
    load_csv(cursor, db, "Team", "prod_data/data/teams.csv")
    load_csv(cursor, db, "Season", "prod_data/data/seasons.csv")
    load_csv(cursor, db, "PlayerTeamHistory", "prod_data/data/player_team_history.csv")
    load_csv(cursor, db, "Game", "prod_data/data/games.csv")
    load_csv(cursor, db, "PlayerGameStats", "prod_data/data/boxscores.csv")
    load_csv(cursor, db, "PlayerSeasonStats", "prod_data/data/player_season_stats.csv")


def db_init():
    print("Initializing database...")
    db = get_db_connection()
    cursor = db.cursor()

    try:
        run_sql_file(cursor, db, "sql/create_tables.sql")
        print("Created tables")
        # run_sql_file(cursor, db, "sql/sample_data.sql")
        # print("Loaded sample data")

        # load production data
        load_prod_data(cursor, db)
        print("Loaded prod data")

    except Exception as e:
        print(
            f"Database initialization error (might already be initialized): {e}")
    finally:
        db.close()
