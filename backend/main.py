import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection, db_init

load_dotenv()

app = Flask(__name__)
CORS(app)

# R6
@app.route("/api/player/season_stats", methods=["GET"])
def season_stats():
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

    keys = ["player_name", "season_id", "team_name", "points_per_game",
            "assists_per_game", "rebounds_per_game", "blocks_per_game"]
    return jsonify([dict(zip(keys, row)) for row in results])


# R7
@app.route("/api/player/game_stats", methods=["GET"])
def game_stats():
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


@app.route("/api/player/game_stats/by_date", methods=["GET"])
def game_stats_for_date():
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

    if not result:
        return jsonify({"message": "No data found"}), 404

    keys = ["date", "opponent", "points", "assists", "rebounds", "blocks"]
    return jsonify(dict(zip(keys, result)))


# R8
@app.route("/api/player/game_stats/by_stat", methods=["GET"])
def best_game_by_stat():
    player_name = request.args.get("player_name")
    stat = request.args.get("stat")

    valid_stats = {"points", "assists", "rebounds", "blocks"}
    if not player_name or not stat or stat not in valid_stats:
        return jsonify({"error": "Missing or invalid parameters"}), 400

    query = f"""
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
    WHERE p.player_name = %s
    ORDER BY pg.{stat} DESC
    LIMIT 1;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (player_name,))
    result = cur.fetchone()
    db.close()

    if not result:
        return jsonify({"message": "No data found"}), 404

    keys = ["date", "opponent", "points", "assists", "rebounds", "blocks"]
    return jsonify(dict(zip(keys, result)))


# R9
@app.route("/api/player/top10", methods=["GET"])
def top_10():
    stat = request.args.get("stat")

    valid_stats = {"points", "assists", "rebounds", "blocks"}
    if not stat or stat not in valid_stats:
        return jsonify({"error": "Missing or invalid parameter"}), 400

    query = f"""
    SELECT 
        p.player_name,
        SUM(pg.{stat}) AS total_{stat}
    FROM PlayerGameStats pg
        JOIN Player p ON pg.player_id = p.player_id
    GROUP BY p.player_name
    ORDER BY total_{stat} DESC
    LIMIT 10;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query)
    results = cur.fetchall()
    db.close()

    keys = ["player_name", f"total_{stat}"]
    return jsonify([dict(zip(keys, row)) for row in results])


if __name__ == "__main__":
    db_init() 

    app.run(host=os.getenv("FLASK_RUN_HOST"),
            port=os.getenv("FLASK_RUN_PORT"), debug=True)
