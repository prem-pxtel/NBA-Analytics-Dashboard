import os
from dotenv import load_dotenv
from __init__ import create_app
from db import db_init

load_dotenv()

app = create_app()

if __name__ == "__main__":
    db_init()
    app.run(host=os.getenv("FLASK_RUN_HOST"),
            port=os.getenv("FLASK_RUN_PORT"), debug=True)


# # ---- Admin only ----
# @app.route("/api/player", methods=["POST"])
# @admin_required()
# def add_player():
#     data = request.get_json()
#     player_id = data.get("player_id")
#     player_name = data.get("player_name")
#     birth_date = data.get("birth_date")
#     position = data.get("position")
#     is_active = data.get("is_active", True)
#     weight = data.get("weight")
#     height = data.get("height")
#     draft_year = data.get("draft_year")

#     if not player_id or not player_name:
#         return jsonify({"error": "Missing player_id or player_name"}), 400

#     query = f"""
#     INSERT INTO Player
#     VALUES ({player_id}, {player_name}, {birth_date}, {position}, {is_active}, {weight}, {height}, {draft_year})
#     """

#     db = get_db_connection()
#     cur = db.cursor()
#     cur.execute(query)
#     db.commit()
#     db.close()

#     return jsonify({"message": "Player added successfully"}), 201


# @app.route("/api/player", methods=["POST"])
# @admin_required()
# def delete_player():
#     data = request.get_json()
#     player_id = data.get("player_id")

#     query = f"DELETE FROM Player WHERE player_id = {player_id}"

#     db = get_db_connection()
#     cur = db.cursor()
#     cur.execute(query)
#     db.commit()
#     db.close()

#     if cur.rowcount == 0:
#         return jsonify({"error": "Player not found"}), 404
#     return jsonify({"message": "Player deleted successfully"}), 200


# if __name__ == "__main__":
#     db_init()

#     app.run(host=os.getenv("FLASK_RUN_HOST"),
#             port=os.getenv("FLASK_RUN_PORT"), debug=True)
