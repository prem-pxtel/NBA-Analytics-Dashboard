import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()


app = Flask(__name__)
CORS(app)


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


@app.route("/api/player/stats_per_season", methods=["GET"])
def stats_per_season():
    player_name = request.args.get("player_name")
    if not player_name:
        return jsonify({"error": "Missing parameters"}), 400
    
    query = """
    SELECT p.player_name,
        s.season_id,
        t.team_name,
        ps.points_per_game,
        ps.assists_per_game,
        ps.rebounds_per_game,
        ps.blocks_per_game
    FROM PlayerSeasonStats ps
        JOIN Season s ON ps.season_id = s.season_id
        JOIN Team t ON ps.team_id = t.team_id
        JOIN Player p ON ps.player_id = p.player_id
    WHERE p.player_name ILIKE %s;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (player_name,))
    results = cur.fetchall()
    db.close()

    keys = ["player_name", "season_id", "team_name", "points_per_game", "assists_per_game", "rebounds_per_game", "blocks_per_game"]
    return jsonify([dict(zip(keys, row)) for row in results])


@app.route("/api/player/stats_per_game", methods=["GET"])
def stats_per_game():
    player_name = request.args.get("player_name")
    if not player_name:
        return jsonify({"error": "Missing parameters"}), 400 

    query = """
    SELECT 
        g.game_date AS date,
    CASE
        WHEN pg.team_id = g.home_team_id THEN away.team_name
        ELSE home.team_name
    END AS opponent,
        pg.points,
        pg.assists,
        pg.rebounds,
        pg.blocks
    FROM PlayerGameStats pg
        JOIN Player p ON pg.player_id = p.player_id
        JOIN Game g ON pg.game_id = g.game_id
        JOIN Team home ON g.home_team_id = home.team_id
        JOIN Team away ON g.away_team_id = away.team_id
    WHERE p.player_name ILIKE %s;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (player_name,))
    results = cur.fetchall()
    db.close()

    keys = ["date", "opponent", "points", "assists", "rebounds", "blocks"]
    return jsonify([dict(zip(keys, row)) for row in results])


@app.route("/api/player/stats_per_game/by_game", methods=["GET"])
def game_stats():
    player_name = request.args.get("player_name")
    date = request.args.get("date")

    if not player_name or not date:
        return jsonify({"error": "Missing parameters"}), 400 

    query = """
    SELECT 
        g.game_date AS date,
    CASE
        WHEN pg.team_id = g.home_team_id THEN away.team_name
        ELSE home.team_name
    END AS opponent,
        pg.points,
        pg.assists,
        pg.rebounds,
        pg.blocks
    FROM PlayerGameStats pg
        JOIN Player p ON pg.player_id = p.player_id
        JOIN Game g ON pg.game_id = g.game_id
        JOIN Team home ON g.home_team_id = home.team_id
        JOIN Team away ON g.away_team_id = away.team_id
    WHERE p.player_name ILIKE %s AND date = %s;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (player_name, date))
    result = cur.fetchone()
    db.close()

    keys = ["date", "opponent", "points", "assists", "rebounds", "blocks"]
    return jsonify(dict(zip(keys, result)))



if __name__ == "__main__":
    # init db
    print("Initializing database...")
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        run_sql_file(cursor, db, "sql/create_tables.sql")
        print("Created tables")
        run_sql_file(cursor, db, "sql/sample_data.sql")
        print("Loaded sample data")
    except Exception as e:
        print(f"Database initialization error (might already be initialized): {e}")
    finally:
        db.close()

    app.run(host=os.getenv("FLASK_RUN_HOST"), port=os.getenv("FLASK_RUN_PORT"), debug=True)

