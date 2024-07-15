import os
from quart import Quart, jsonify
from databases import Database
from dotenv import load_dotenv

load_dotenv()

app = Quart(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

@app.before_serving
async def startup():
    await database.connect()

@app.after_serving
async def shutdown():
    await database.disconnect()

@app.route("/guilds")
async def get_guilds():
    query = "SELECT * FROM guild"
    results = await database.fetch_all(query=query)
    return jsonify([dict(result) for result in results])

@app.route("/players")
async def get_players():
    query = "SELECT * FROM player"
    results = await database.fetch_all(query=query)
    return jsonify([dict(result) for result in results])

@app.route("/characters")
async def get_characters():
    query = """
    SELECT c.*, cb.name as base_name, cb.class_id, p.name as player_name, s.name as spec_name
    FROM "character" c
    JOIN character_base cb ON c.character_base_id = cb.id
    JOIN player p ON cb.player_id = p.id
    JOIN spec s ON c.spec_id = s.id
    """
    results = await database.fetch_all(query=query)
    return jsonify([dict(result) for result in results])

@app.route("/raid-effects")
async def get_raid_effects():
    query = "SELECT * FROM raid_effect"
    results = await database.fetch_all(query=query)
    return jsonify([dict(result) for result in results])

@app.route("/raid-effect-providers")
async def get_raid_effect_providers():
    query = """
    SELECT rep.*, re.name as effect_name, c.name as class_name, s.name as spec_name
    FROM raid_effect_provider rep
    JOIN raid_effect re ON rep.raid_effect_id = re.id
    LEFT JOIN class c ON rep.class_id = c.id
    LEFT JOIN spec s ON rep.spec_id = s.id
    """
    results = await database.fetch_all(query=query)
    return jsonify([dict(result) for result in results])

if __name__ == "__main__":
    app.run(debug=True)
