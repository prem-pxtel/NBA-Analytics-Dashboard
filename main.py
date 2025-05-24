import psycopg2

host = "localhost"
port = 5432
database = "groupproject"
user = "team"

db = psycopg2.connect(host=host, port=port, database=database, user=user)
cursor = db.cursor()
print("Connected")

create_table = """
CREATE TABLE IF NOT EXISTS players (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
name VARCHAR NOT NULL);"""
cursor.execute(create_table)
db.commit()

insert_players_query = """INSERT INTO players(name) VALUES (%s);"""
cursor.execute(insert_players_query, ("Lebron James",))
db.commit()

read_players_query = """SELECT * FROM players"""
cursor.execute(read_players_query)
rows = cursor.fetchall()
print("Here are the players", rows)

