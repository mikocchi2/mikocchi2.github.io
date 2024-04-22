import requests
import urllib
import json


########################################################################
#                                                                      #
#   Everything that has to do with talking to the API                  #
#                  And getting game data                               #
#                                                                      #
########################################################################

"""
                                                                        
10            timelineDto['info']['frames'][minute]['participantFrames'][pid]       pid 1-10

"""


# info
api_key = 'RGAPI-418f712d-27c1-41e4-9a58-7536fdf38400'
myPuuid = 'Se279KIaijMJdjvNvUV7a4lRYffphvLCGOcHqbJctzA1pzMs6WZJWf5MVx5BDlW-JzSS40-CLG_lEA'
        # 7T00IGWidbGmYzlML6f9pAQ3PMMk1zbCTlOiID78sXIe
acc_id = "cFxVignU3b82QlL4th5R7P7gHM8LS8R8mwSwFQqKqSQUxi8"
id = "LoD1aSEh9xnfjieJ0V36-vM47Cy7F7rDeFfv3qh--fkYk2M"

# technical
headers = {"X-Riot-Token": api_key}
max_games = 99
current_patch = '14.7'

"""
game_name = "Tryndamere"
tag_line = "L9 FF"
otp = 'Quinn'

drugari = [('Shiro und Kuro','Ugrin'),
           ('agicat2','mache'),
           ('Dikshot','EUNE'), 
           ('Tryndamere','L9 FF')]


useful = ['champLevel','gameEndedInSurrender','goldEarned','wardsPlaced','damageDealtToTurrets']
"""


  

# setup
def get_puuid(game_name,tag_line):
    tag = urllib.parse.quote(tag_line)
    summoner = urllib.parse.quote(game_name)
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner}/{tag}?api_key={api_key}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        player_info = response.json()
        puuid = player_info['puuid']
    else:
        print(f"Error fetching player data: {response.status_code}")
        return None
    return puuid

def get_recent_matches(puuid,count):
    matches_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={count}&api_key={api_key}"
    matches = requests.get(matches_url, headers=headers).json()
    return matches

def get_patch_matches(puuid):
    matches_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count={max_games}&api_key={api_key}"
    matches = requests.get(matches_url, headers=headers).json()
    patch_games = []
    for gm in matches:
        if get_patch(gm) == current_patch:
            patch_games.append(gm)
        else: break
    return patch_games


def last_game(puuid):
    return get_recent_matches(puuid,1)[0]

def get_participants(match_id):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'
    match = requests.get(url,headers=headers).json()
    participants = match['info']['participants']
    return participants

# run on matches[i]
def get_timeline(match_id):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline?api_key={api_key}'
    timeline = requests.get(url,headers=headers).json()
    return timeline
def get_matchDto(match_id):                                         # ako treba metadata
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'
    match = requests.get(url,headers=headers).json()
    return match




    my = []
    enemy = []
    did_i_win = True
    for i in range(10):
        if participants[i]['puuid'] == myPuiid:
            did_i_win = participants[i]['win']
            break
    if did_i_win == True:
        for i in range(10):
            champ = participants[i]['championName']
            win = participants[i]['win']
            if win == True:
                my.append(champ)
            else: enemy.append(champ)
    if did_i_win == False:
        for i in range(10):
            champ = participants[i]['championName']
            win = participants[i]['win']
            if win == True:
                enemy.append(champ)
            else: my.append(champ)
    teams = (my,enemy,did_i_win)
    return teams

def get_teams(match_id,puuid,print_ = False):

    parts = get_participants(match_id)

    for i in range(10):
        if parts[i]['puuid'] == puuid:
            myIndex = i

    me = parts[myIndex]

    if myIndex < 5:

        myTop = parts[0]
        myJungler = parts[1]
        myMid = parts[2]
        myAdc = parts[3]
        mySupp = parts[4]

        enemyTop = parts[5]
        enemyJungler = parts[6]
        enemyMid = parts[7]
        enemyAdc = parts[8]
        enemySupp = parts[9]

    else:
        myTop = parts[5]
        myJungler = parts[6]
        myMid = parts[7]
        myAdc = parts[8]
        mySupp = parts[9]

        enemyTop = parts[0]
        enemyJungler = parts[1]
        enemyMid = parts[2]
        enemyAdc = parts[3]
        enemySupp = parts[4]

    my = [myTop, myJungler, myMid, myAdc, mySupp]
    enemy = [enemyTop, enemyJungler, enemyMid, enemyAdc, enemySupp]

    if print_:
        print(f"{myTop['championName']:15} | {myJungler['championName']:15} | {myMid['championName']:15} | {myAdc['championName']:15} | {mySupp['championName']:15} | ")
        print(f"{enemyTop['championName']:15} | {enemyJungler['championName']:15} | {enemyMid['championName']:15} | {enemyAdc['championName']:15} | {enemySupp['championName']:15} |")

    return(my,enemy,(me,myIndex))

def gameDuration(match_id):
        match = get_matchDto(match_id)
        gameDur = round(int(match['info']['gameDuration'])/60)
        return gameDur
def get_patch(match_id): # 14.24
        match = get_matchDto(match_id)
        patch = match['info']['gameVersion']
        first_dot = patch.find('.')                  # Find the first dot
        second_dot = patch.find('.', first_dot + 1)  # Find the second dot after the first
        if second_dot != -1:
            return patch[:second_dot]
        return patch



# HERE WE GO AGAIN
def get_me(participants, puuid):
    
    for i in range(10):
        if participants[i]['puuid'] == puuid:
            return participants[i]
    return None  # Explicitly return None if no participant matches

def get_me_and_laner(match_id, puuid):
    parts = get_participants(match_id)
    me = None
    laner = None

    # Find the player index and details
    for i, participant in enumerate(parts):
        if participant['puuid'] == puuid:
            myIndex = i
            me = participant
            break  # Stop the loop once the player is found

    if me is None:
        raise ValueError("Player not found")  # Or return None, None if you prefer not to raise an exception

    # Determine the opposing laner based on index
    if myIndex < 5:
        laner = parts[myIndex + 5]
    else:
        laner = parts[myIndex - 5]

    return (me, laner)


# fuck this
def get_summoners_in_elo(tier,division,page): # [ of summoner_ids to be converted into puuids ]
    
    url = f'https://eun1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}&api_key={api_key}'
    response = requests.get(url,headers=headers).json()
    return [ summoner['summonerId'] for summoner in response ]

def summoner_ids_to_puuids(summoner_ids):
    puuids = []
    for id in summoner_ids:
        summonerDto = get_SummonerDTO(id)
        try:
            puuid = summonerDto['puuid']
            puuids.append(puuid)
        except Exception as e:
            print(e)
            continue
    return puuids
    
def get_SummonerDTO(summoner_id):
    url = f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}'
    summoner = requests.get(url,headers=headers).json()
    return summoner

