import os
from quart import Quart, jsonify
from databases import Database
from dotenv import load_dotenv

load_dotenv()

app = Quart(__name__)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

@app.before_serving
async def startup():
    await database.connect()

@app.after_serving
async def shutdown():
    await database.disconnect()

@app.route("/")
async def hello():
    return jsonify({"message": "Welcome to the Warcraft Raid Organizer API"})

@app.route("/players")
async def get_players():
    query = "SELECT * FROM players"
    results = await database.fetch_all(query=query)
    return jsonify([dict(result) for result in results])

if __name__ == "__main__":
    app.run(debug=True)
