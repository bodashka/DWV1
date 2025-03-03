from flask import Flask, request, jsonify
from flask_cors import CORS
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
ATLAS_URI = os.getenv("ATLAS_URI")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Connect to MongoDB
client = pymongo.MongoClient(ATLAS_URI)
db = client["movies_db"]
collection = db["highest_grossing_films"]

@app.route("/movies", methods=["GET"])
def get_movies():
    query = request.args.get("title", "")
    search_filter = {"title": {"$regex": query, "$options": "i"}} if query else {}
    movies = list(collection.find(search_filter, {"_id": 0}))
    return jsonify(movies)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
