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
        ps.season_id,
        t.team_name,
        ps.total_points,
        ps.avg_assists,
        ps.avg_rebounds,
        ps.avg_blocks
    FROM PlayerSeasonStatsMV ps
        JOIN Team t ON ps.team_id = t.team_id
        JOIN Player p ON ps.player_id = p.player_id
    WHERE p.player_name ILIKE %s
    ORDER BY ps.season_id DESC;
    """

    print("ok lets go with query")

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (f"%{player_name}%",))
    results = cur.fetchall()
    print(f"Found {len(results)} rows for '{player_name}'")
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
    WHERE p.player_name ILIKE %s AND g.game_date = %s;
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


# R10
@player_stats_bp.route("/draft_by_team", methods=["GET"])
@jwt_required()
def draft_by_team():
    team_name = request.args.get("team_name")
    start_year = request.args.get("start_year")
    end_year = request.args.get("end_year")

    if not all([team_name, start_year, end_year]):
        return jsonify({"error": "Missing parameter"}), 400
    
    query = """
        SELECT 
            p.player_name,
            p.draft_year,
            p.position,
            CASE WHEN p.is_active THEN 'Yes' ELSE 'No' END AS active_status
        FROM Player p
                JOIN PlayerTeamHistory pt ON p.player_id = pt.player_id
                JOIN Team t ON pt.team_id = t.team_id
        WHERE t.team_name = %s
            AND p.draft_year BETWEEN %s AND %s
        ORDER BY p.draft_year;
    """

    db = get_db_connection()
    cur = db.cursor()
    cur.execute(query, (team_name, start_year, end_year))
    results = cur.fetchall()
    db.close() 

    keys = ["player_name", "draft_year", "position", "active_status"]
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
    
    keys = ["opponent", "points", "assists", "rebounds", "blocks"]
    return jsonify(dict(zip(keys, result)))


# advanced feature 3 - updating PlayerGameStats
@player_stats_bp.route("/update_game_stats", methods=["POST"])
@admin_required
def update_game_stats():
    data = request.get_json()

    player_name = data.get("player_name")
    game_id = data.get("game_id")

    if not player_name or not game_id:
        return jsonify({"error": "Missing player_name or game_id"}), 400
    
    columns = ["points", "assists", "rebounds", "blocks", "FGA", "FGM", "FTA", "FTM"]
    update_cols = {k: v for k, v in data.items() if k in columns and v is not None}
    if not update_cols:
        return jsonify({"error": "No fields to update"})


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
    set_clause = ""
    values = []
    for col, val in update_cols.items():
        set_clause += (f"{col} = %s\n")
        values.append(val)

    update_query = """
    UPDATE PlayerGameStats
    SET {set_clause}
    WHERE player_id = %s AND game_id = %s;
    """

    cur.execute(update_query, tuple())
    if cur.rowcount == 0:
            return jsonify({"error": "Player stats not found for this game"}), 404
        
    db.commit()
    db.close()

    return jsonify({"message": "Player game stats updated successfully"}), 200


