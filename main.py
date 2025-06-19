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
        sql = file.read()

    return [q.strip() for q in sql.split(';') if q.strip()]


def test_sample(player_id: int):
    # insert sample data
    run_sql_file("sql/sample_data.sql")
    print("Sample data loaded")

    # load queries and set param for each
    test_queries = load_query("sql/test-sample.sql")
    params_list = [
        {"player_id": 1, "season_id": 2003},   # R6
        {"player_id": 1, "game_id": 1},     # R7
        {"player_id": 1, "stat": "points"},  # R8
        {}                                  # R9
    ]

    results = []

    for i, query in enumerate(test_queries):
        param = params_list[i]
        if i == 0:
            query = query.format(player_id=param['player_id'], season_id=param['season_id'])
        elif i == 1:
            query = query.format(player_id=param['player_id'], game_id=param['game_id'])

        elif i == 2:
            query = query.format(player_id=param['player_id'], stat=param['stat'])
        elif i == 3:
            pass

        cursor.execute(query, param)
        results.append(cursor.fetchall())

    # print result
    for test_num, r in enumerate(results):
        print(f"{test_num}\t\t{r}")

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
