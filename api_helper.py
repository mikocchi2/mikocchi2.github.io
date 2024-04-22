from setup import *
from analysis import *

def process_summoner(summoner,tag):
    filename = f'users/{summoner}.json'
    puuid = get_puuid(summoner,tag)
    recent = get_recent_matches(puuid,2)
    for match in recent:
        print('ok')
        analyze_game_end_api(match,puuid,filename)

def json_for_frontend(filename):
    games_stats = {}
    with open(f"users/{filename}.json", "r") as file:
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
    return games_stats