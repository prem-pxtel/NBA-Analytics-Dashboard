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


def test_sample(player_id: int):
    # insert sample data
    run_sql_file("sql/sample_data.sql")
    print("Sample data loaded")

    # test R6
    test_query = load_query("sql/test-sample.sql")
    cursor.execute(
        test_query,
        {"player_id": 1, "season_id": 1, "game_id": 1, "stat": "points"}
    )
    results = cursor.fetchall()
    # print result
    for r in results:
        print(r)

    return results


if __name__ == "__main__":
    load_dotenv()

    # connect to database
    db = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER")
        # password=os.getenv("DB_PWD")
    )
    cursor = db.cursor()
    print("Connected to database")

    # create tables
    run_sql_file("sql/create_tables.sql")
    print("Created tables")

    # run test
    test_sample(player_id=1)
