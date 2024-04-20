from flask import Flask, jsonify, json
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Data to serve with our API

games_stats = {}
with open("games.json", "r") as file:
    data = json.load(file)
    for game_id, stats in data.items():
        games_stats[game_id] = {
            "champ": stats['champ'],
            "lanerChamp" :stats['lanerChamp'],
            "cs_per_minute": stats['cs_per_minute'],
            "gold_difference": stats['gold_difference'],
            "cs_difference": stats['cs_difference'],
            "win": stats.get('win', False)
        }
        


# A route to return all of the available entries in our catalog.
@app.route('/api/games', methods=['GET'])
def api_all():
    return jsonify(games_stats)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
