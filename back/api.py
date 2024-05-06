from flask import Flask, jsonify, json, request, redirect, url_for
from flask_cors import CORS  # Import CORS
import setup
from game import Game

app = Flask(__name__)
CORS(app)

global_stats = []

@app.route('/api/key', methods=['GET'])
def api_all():
    key = request.args.get('key', 'Default Game')
    setup.update_api_key(key)

@app.route('/api/results')
def stats_display():
    print('poslao results')
    return jsonify(global_stats)

@app.route('/', methods=['GET'])
def test():
    return "hello acko"


@app.route('/api/user', methods=['GET'])
def summonerko():
    amount = request.args.get('amount', '20')
    game_name = request.args.get('game_name', 'Default Game')  # Default value is 'Default Game'
    tagline = request.args.get('tagline', 'No Tagline Provided')  # Default value is 'No Tagline Provided'
    puuid = setup.get_puuid(game_name,tagline)

    recent = Game.recent_games(puuid,amount)
    for game in recent:
        global_stats.append(game.to_dict())
    return jsonify(global_stats)

if __name__ == '__main__':
    app.run(debug=True)