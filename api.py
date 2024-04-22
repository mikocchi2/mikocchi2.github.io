from flask import Flask, jsonify, json, request, redirect, url_for
from flask_cors import CORS  # Import CORS
from api_helper import *

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Data to serve with our API

global_stats = None

def get_gm_stats():
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
    game_stats = get_gm_stats()
    return jsonify(game_stats)


@app.route('/api/user', methods=['GET'])
def summonerko():
    game_name = request.args.get('game_name', 'Default Game')  # Default value is 'Default Game'
    tagline = request.args.get('tagline', 'No Tagline Provided')  # Default value is 'No Tagline Provided'
    
    print(game_name,tagline)
    response = f"Game Name: {game_name}, Tagline: {tagline} USPIJEH U KOMUNIKACIJI"
    process_summoner(game_name,tagline)
    stats = json_for_frontend(game_name)
    global global_stats
    global_stats = stats
    return redirect(url_for('stats_display'))

@app.route('/api/results')
def stats_display():
    print('poslao results')
    return jsonify(global_stats)




# Run the application
if __name__ == '__main__':
    app.run(debug=True)
