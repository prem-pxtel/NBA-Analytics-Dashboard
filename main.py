import os
import psycopg2
from dotenv import load_dotenv


def run_sql_file(path: str):
    with open(path, 'r') as sql_file:
        sql = sql_file.read()
        cursor.execute(sql)
        db.commit()


def load_query(path: str):
    with open(path, 'r') as file:
        return file.read()


def main():
    load_dotenv()

    # connect to database
    db = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER")
    )
    cursor = db.cursor()
    print("Connected to database")

    # create tables
    run_sql_file("sql/create_tables.sql")
    print("Created tables")

    # insert sample data
    run_sql_file("sql/sample_data.sql")
    print("Sample data loaded")

    # test R6
    # r6_query = load_query()


if __name__ == "__main__":
    main()
