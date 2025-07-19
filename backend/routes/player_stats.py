from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from db import get_db_connection
from utils import admin_required

player_stats_bp = Blueprint('player_stats', __name__, url_prefix='/api/player')

# R6
@player_stats_bp.route("/season_stats", methods=["GET"])
@jwt_required()
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
@player_stats_bp.route("/game_stats", methods=["GET"])
@jwt_required()
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


@player_stats_bp.route("/game_stats/by_date", methods=["GET"])
@jwt_required()
def game_stats_for_date():
    player_name = request.args.get("player_name")
    date = request.args.get("date")

    if not player_name or not date:
        return jsonify({"error": "Missing parameter"}), 400

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
@player_stats_bp.route("/game_stats/by_stat", methods=["GET"])
@jwt_required()
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
@player_stats_bp.route("/top10", methods=["GET"])
@jwt_required()
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


# advanced feature 2 - most recent game for a player
@player_stats_bp.route("/recent_game_stats", methods=["GET"])
@jwt_required()
def recent_game_stats():
    player_name = request.args.get("player_name")

    if not player_name:
        return jsonify({"error": "Missing parameter"}), 400
    
    query = """
    SELECT 
        date,
        opponent,
        points,
        assists,
        rebounds,
        blocks 
    FROM MostRecentGame
    WHERE player_name ILIKE %s
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (player_name,))
    result = cur.fetchone()
    db.close()

    if not result:
        return jsonify({"message": "No data found"}), 404
    
    keys = ["player_name"]
    return jsonify(dict(zip(keys, result)))


# advanced feature 3 - updating PlayerGameStats
@player_stats_bp.route("/update_gamestats", methods=["GET"])
@admin_required
def update_game_stats():
    player_name = request.args.get("player_name")
    game_id = request.args.get("game_id")
    team_id = request.args.get("team_id")
    points = request.args.get("points")
    assists = request.args.get("assists")
    rebounds = request.args.get("rebounds")
    blocks = request.args.get("blocks")
    FGA = request.args.get("FGA")
    FGM = request.args.get("FGM")
    FTA = request.args.get("FTA")
    FTM = request.args.get("FTM")

    if not player_name or not game_id:
        return jsonify({"error": "Missing player_name or game_id"}), 400
    
    db = get_db_connection()
    cur = db.cursor()
    

    # Get player_id from player_name
    get_player_id_query = """
        SELECT player_id
        FROM Player
        WHERE player_name ILIKE %s
    """

    cur.execute(get_player_id_query, (player_name))
    player = cur.fetchone()
    if not player:
        return jsonify({"error": "Player not found"}), 404
    player_id = player[0]

    # Update table
    update_query = """
    UPDATE PlayerGameStats
    SET 
        team_id = %s,
        points = %s,
        assists = %s,
        rebounds = %s,
        blocks = %s,
        FGA = %s,
        FGM = %s,
        FTA = %s,
        FTM = %s
    WHERE player_id = %s AND game_id = %s;
    """

    cur.execute(update_query, (team_id, points, assists, rebounds, blocks, FGA, FGM, FTA, FTM, player_id, game_id))
    if cur.rowcount == 0:
            return jsonify({"error": "Player stats not found for this game"}), 404
        
    db.commit()
    db.close()
    
    return jsonify({"message": "Player game stats updated successfully"}), 200


