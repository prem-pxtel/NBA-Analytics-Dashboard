import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER")
        # password=os.getenv("DB_PWD")
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


def test_sample(cursor, player_id: int, season_id: int, game_id: int, stat: str):
    # load queries
    test_queries = load_query("sql/test-sample.sql")

    results = []

    for i, query in enumerate(test_queries):
        if i == 0:
            query = query.format(player_id=player_id, season_id=season_id)
        elif i == 1:
            query = query.format(player_id=player_id, game_id=game_id)
        elif i == 2:
            query = query.format(player_id=player_id, stat=stat)
        elif i == 3:
            pass

        cursor.execute(query)
        results.append(cursor.fetchall())

    # print result
    for test_num, r in enumerate(results):
        print(f"{test_num}\t\t{r}")

    return results

# API endpoint


@app.route("/api/player_stats", methods=["GET"])
def get_player_stats():
    # get query parameters
    try:
        player_id = int(request.args.get("player_id"))
        season_id = int(request.args.get("season_id"))
        game_id = int(request.args.get("game_id"))
        stat = request.args.get("stat")
    except:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    # connect to database
    db = get_db_connection()
    cursor = db.cursor()
    print("Connected to database")

    # create & load tables
    run_sql_file(cursor, db, "sql/create_tables.sql")
    print("Created tables")
    run_sql_file(cursor, db, "sql/sample_data.sql")
    print("Loaded tables")

    # run test
    results = test_sample(cursor, player_id, season_id, game_id, stat)

    db.close()
    return jsonify({
        "r6_player_season_stats": results[0],
        "r7_player_game_stats": results[1],
        "r8_best_game_by_stat": results[2],
        "r9_all_time_top_scorers": results[3]
    })


if __name__ == "__main__":
    app.run(host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))
