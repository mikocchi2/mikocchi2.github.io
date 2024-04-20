from setup import *

########################################################################################
#                                                                                      #
#      T H E         P O I N T   :    WHO WAS BETTER   after    GAME    /   LANE       #
#                                                                                      #
#                                ME    OR     LANER?                                   #
#                                                                                      #
########################################################################################




# sva analiza treba da mi je containovana unutar ovih 3 funkcija
# ove 3 treba da mi daju statistical data, a svaki subsequent function treba da 
# bude statistics being done on these data


# F L O W:      analzye end + analyze min pa se racuna AC score ili whatever pa ide writing to json
# make a seperate function that calls end,15,and each score
# just json assignment



def analyze_min(match_id,min):

    def find_id(timelineDto,puuid):
        for i in timelineDto['info']['participants']:
            if i['puuid'] == puuid:
                return i['participantId']
            
    me,laner = get_me_and_laner(match_id)
    
    myPuuid = me['puuid']
    lanerPuuid = laner['puuid']

    matchDto =  get_matchDto(match_id)
    timelineDto = get_timeline(match_id)
    minute = min
    pid = str(find_id(timelineDto,myPuuid))
    laner_pid = str(find_id(timelineDto,lanerPuuid))

    minut = timelineDto['info']['frames'][minute]

    my_stats_at_min = timelineDto['info']['frames'][minute]['participantFrames'][pid]
    laner_stats_at_min = timelineDto['info']['frames'][minute]['participantFrames'][laner_pid]

    totalGold = my_stats_at_min['totalGold']
    xp = my_stats_at_min['xp']
    level = my_stats_at_min['level']
    cs = my_stats_at_min['jungleMinionsKilled'] + my_stats_at_min['minionsKilled']
    cspm = cs / minute
    gpm = totalGold / minute



    laner_totalGold = laner_stats_at_min['totalGold']
    laner_xp = laner_stats_at_min['xp']
    laner_level = laner_stats_at_min['level']
    laner_cs = laner_stats_at_min['jungleMinionsKilled'] + laner_stats_at_min['minionsKilled']
    laner_cspm = laner_cs / minute
    laner_gpm = laner_totalGold / minute

    gold_diff = totalGold - laner_totalGold
    level_diff = level - laner_level
    cs_diff = cs - laner_cs
    cspm_diff = cspm - laner_cspm
    gpm_diff = gpm - laner_gpm


    print_str = f'gold diff: {gold_diff}\tlevel diff: {level_diff}\tcs diff: {cs_diff}\n'
    print(print_str)

    return gold_diff


# ako hoces da dodajes stats u JSON nakon definitivne strukture, 
# ili promeni json u novi za nove gejmove (major change)
# ili dodaj novi key u svaki entry i stavi ga na null
def analyze_game_end(match_id,puuid):

    # useless
    def is_between(x, a, b):
        return a <= x <= b
    def calculate_gold_gap(gold_difference):
        gold_gap = None
        if is_between(gold_difference,0,500): gold_gap = 'even'                                 #6         
        elif is_between(gold_difference,500,1000): gold_gap = 'barely ahead'                    #7
        elif is_between(gold_difference,1001,2000): gold_gap = 'ahead'                          #8
        elif is_between(gold_difference,2001,3000): gold_gap = 'won'                            #9
        elif gold_difference >= 3001: gold_gap = 'gap'                                          #10

        elif is_between(gold_difference,-500,0): gold_gap = 'even'                              #5
        elif is_between(gold_difference,-1000,-501): gold_gap = 'slightly_behind'               #4
        elif is_between(gold_difference,-2000,-1001): gold_gap = 'behind'                       #3
        elif is_between(gold_difference,-3000,-2001): gold_gap = 'lost'                         #2
        elif gold_difference <= 3001: gold_gap = 'got gapped'                                   #1
        return gold_gap
    def calculate_lvl_gap(lvl_diff):
        lvl_gap = None
        if lvl_diff == 0:   lvl_gap = 'even'                                                    

        elif lvl_diff == 1: lvl_gap = 'ahead'
        elif lvl_diff == 2: lvl_gap = 'won'
        elif lvl_diff > 2:  lvl_gap = 'gap'

        if lvl_diff == -1:  lvl_gap = 'behind'
        if lvl_diff == -2:  lvl_gap = 'lost'
        if lvl_diff < -2:   lvl_gap = 'got gapped'
        return lvl_gap

    # setup
    me,laner = get_me_and_laner(match_id,puuid)
    print(f'{me['championName']} vs {laner['championName']}')
    gameDur = gameDuration(match_id)
    patch = get_patch(match_id)


    # my game stats
    champ = me['championName']
    lanerChamp = laner['championName']

    cs = me['totalMinionsKilled']
    cspm = cs/gameDur
    wards_placed = me['wardsPlaced']
    vision_score = me['visionScore']
    dead = me['totalTimeSpentDead']/60
    percentDead = round(dead/gameDur*100)

    kills = me['kills']
    assists = me['assists']
    deaths = me['deaths']
    kda = (kills+assists) / deaths if deaths != 0 else "perfect"

    # lane comparation stats
    gold_difference = me['goldEarned'] - laner['goldEarned']
    gpm = me['goldEarned']/gameDur
    cs_diff = me['totalMinionsKilled'] - laner['totalMinionsKilled']
    lvl_diff = me['champLevel'] - laner['champLevel']
    turret_dmg_diff = me['damageDealtToTurrets'] - laner['damageDealtToTurrets']  
    total_dmg_diff = me['totalDamageDealtToChampions'] - laner['totalDamageDealtToChampions']
    vision_diff = me['visionScore'] - laner['visionScore']

    # analyses
    acScore = None
    acScore_difference = None

    did_i_win = me['win']
    

    # json stats
    game_stats = {
        match_id :
        {
            'myPuuid':puuid,
            'champ': champ,
            'lanerChamp': lanerChamp,
            'patch': patch,
            'ac_score': acScore,
            'ac_score_difference': acScore_difference,
            'win': did_i_win,
            'cs': cs,
            'cs_per_minute': cspm,
            'wards_placed': wards_placed,
            'vision_score': vision_score,
            'time_spent_dead_minutes': dead,
            'percent_time_dead': percentDead,
            'kills': kills,
            'assists': assists,
            'deaths': deaths,
            'kda': kda,
            'gold_difference': gold_difference,
            'gold_per_minute': gpm,
            'cs_difference': cs_diff,
            'level_difference': lvl_diff,
            'turret_damage_difference': turret_dmg_diff,
            'total_damage_difference': total_dmg_diff,
            'vision_score_difference': vision_diff
        }
    }

    # writing to json
    file_name = 'games.json'
    try:
        # First, try to load existing data
        with open(file_name, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If not found, start a new dictionary
        data = {}

   
    data.update(game_stats)  # Update the dictionary with new game stats

    # Write back to the file
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


    # finally
    print(f'{percentDead:.2f}%')
    print(calculate_gold_gap(gold_difference),calculate_lvl_gap(lvl_diff))
    #print(f'gold diff: {gold_difference}\nlvl diff: {lvl_diff}\ncs_diff: {cs_diff} cs:{cs}\nturret dmg diff: {turret_dmg_diff}\ntotal dmg dif: {total_dmg_diff}\nvision diff: {vision_diff}\n wards: {wards_placed}\n')
    return (gold_difference,wards_placed,total_dmg_diff)





def ac_score(match_id, my_puuid): # ac score za gejm
    # Fetch teams based on match_id and my_puuid, separating into 'my' and 'enemy' teams
    my, enemy = get_teams(match_id, my_puuid, False)
    all_parts = my + enemy

    total_kills_my = sum(player['kills'] for player in my)
    total_kills_enemy = sum(player['kills'] for player in enemy)

    gold_scores = {}
    kp_scores = {}

    for player in all_parts:
        puuid = player['puuid']
        team_kills = total_kills_my if player in my else total_kills_enemy
        kp_score = (player['kills'] + player['assists']) / team_kills if team_kills > 0 else 0

        gold_scores[puuid] = player['goldEarned']
        kp_scores[puuid] = kp_score

    ranked_by_gold = sorted(gold_scores, key=gold_scores.get, reverse=True)
    ranked_by_kp = sorted(kp_scores, key=kp_scores.get, reverse=True)

    normalized_gold_rank = {puuid: 10 - i for i, puuid in enumerate(ranked_by_gold)}
    normalized_kp_rank = {puuid: 10 - i for i, puuid in enumerate(ranked_by_kp)}

    final_scores = {}
    for player in all_parts:
        puuid = player['puuid']
        average_rank = (normalized_gold_rank[puuid] + normalized_kp_rank[puuid]) / 2
        final_scores[puuid] = (player['championName'], average_rank)

    # Ensure to use my_puuid to fetch your champion's name and score
    your_champion, your_score = final_scores.get(my_puuid, ("Unknown Champion", "No Score"))
    print(f"Debug: Your Champion: {your_champion}, Your Score: {your_score}")

    return final_scores







recent = get_recent_matches(myPuuid,10)
for i in range(10):
    analyze_game_end(recent[i],myPuuid)