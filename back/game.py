from setup import *
from collections import defaultdict
import time


class Game:

    def __init__(self,puuid,match_id) -> None:
        self.puuid = puuid
        self.match_id = match_id
        me,laner = get_me_and_laner(match_id,puuid)
        self.me = me
        self.laner = laner
        self.matchup = f'{me['championName']} vs {laner['championName']}'
        self.matchDto =  get_matchDto(match_id)
        self.timelineDto = get_timeline(match_id)
        self.participants = self.matchDto['info']['participants']
        self.win = me['win']
        self.min10 = Minut(10,self)
        self.min15 = Minut(15,self)
        self.end = None

    def __str__(self):
        return f'10:{self.min10.__str__()}\n15:{self.min15.__str__()}\n'

    def __repr__(self):
        return f"Game('{self.puuid}', {self.match_id})"
    
    def __eq__(self, other):
        return self.match_id == other.match_id and self.puuid == other.puuid

    def to_dict(self):
        return {
            "match_id":self.match_id,
            "champ":self.me['championName'],
            "laner":self.laner['championName'],
            "win":self.win,
            "gold_grade":self.gold_difference_grade(),
            "10":self.min10.to_dict(),
            "15":self.min15.to_dict()
        }


    def recent_games(puuid,count):
        recent = get_recent_matches(puuid,count)
        time.sleep(10)
        games = [Game(puuid,game) for game in recent]
        return games

    def kp_analysis(self):
        print("hehe")
        minutes = {}
        kills = defaultdict(int)  # Initialize the kills dictionary outside the loop
        assists = defaultdict(int)  # Initialize the assists dictionary outside the loop

        for minute in range(16):  # Assuming your frames are indexed starting at 0
            if minute < len(self.timelineDto['info']['frames']):
                team_kills = {1: 0, 2: 0}  # To track kills by team for the current minute

                for event in self.timelineDto['info']['frames'][minute]['events']:
                    if event['type'] == 'CHAMPION_KILL':
                        # Update kills count
                        if 'killerId' in event:
                            killer_id = event['killerId']
                            kills[killer_id] += 1
                            # Increment team kills
                            team = 1 if killer_id <= 5 else 2
                            team_kills[team] += 1

                        # Update assists count
                        if 'assistingParticipantIds' in event:
                            for assistant in event['assistingParticipantIds']:
                                assists[assistant] += 1

                # Calculate kill participation for this minute
                kp = {}
                for player_id in range(1, 11):
                    team = 1 if player_id <= 5 else 2
                    if team_kills[team] > 0:  # Prevent division by zero
                        player_kp = (kills.get(player_id, 0) + assists.get(player_id, 0)) / team_kills[team]
                        kp[player_id] = round(player_kp * 100, 2)  # Convert to percentage

                # Store results for this minute
                minutes[minute] = {
                    'kills': dict(kills),
                    'assists': dict(assists),
                    'kill_participation': kp
                }

        # Print cumulative kill participation for each player at the end
        print("Cumulative Kill Participation (%):")
        for player_id in range(1, 11):
            team = 1 if player_id <= 5 else 2
            final_team_kills = sum(kills[player] for player in range((team - 1) * 5 + 1, team * 5 + 1))
            if final_team_kills > 0:
                final_kp = ((kills[player_id] + assists[player_id]) / final_team_kills) * 100
                print(f"Player ID {player_id}: {round(final_kp, 2)}%")

        return minutes

    def gold_difference_grade(self):
        gold_diff = self.min15.gold_diff

        if gold_diff <= -3000:
            grade = 0
        elif -3000 < gold_diff <= -2000:
            grade = 1
        elif -2000 < gold_diff <= -1500:
            grade = 2
        elif -1500 < gold_diff <= -1000:
            grade = 3
        elif -1000 < gold_diff <= -500:
            grade = 4
        elif -500 < gold_diff <= 500:
            grade = 5
        elif 500 < gold_diff <= 1000:
            grade = 6
        elif 1000 < gold_diff <= 1500:
            grade = 7
        elif 1500 < gold_diff <= 2000:
            grade = 8
        elif 2000 < gold_diff <= 3000:
            grade = 9
        elif gold_diff > 3000:
            grade = 10

        return grade
    def gold_difference_grade_avg(self):
        gold_diff = self.min15.avg_gold_diff

        if gold_diff <= -3000:
            grade = 0
        elif -3000 < gold_diff <= -2000:
            grade = 1
        elif -2000 < gold_diff <= -1500:
            grade = 2
        elif -1500 < gold_diff <= -1000:
            grade = 3
        elif -1000 < gold_diff <= -500:
            grade = 4
        elif -500 < gold_diff <= 500:
            grade = 5
        elif 500 < gold_diff <= 1000:
            grade = 6
        elif 1000 < gold_diff <= 1500:
            grade = 7
        elif 1500 < gold_diff <= 2000:
            grade = 8
        elif 2000 < gold_diff <= 3000:
            grade = 9
        elif gold_diff > 3000:
            grade = 10

        return grade
    

    """
        participants = self.timelineDto['info']['participants']
        print(participants[0].keys())
        
        for key, val in kills.items():
            for i in range(10):
                if key == participants[i]['participantId']:
                    puuid = participants[i]['puuid']
                    print(puuid,val)
        """
                  





class Minut:
    def __init__(self, minute: int, game: Game) -> None:
        # Call to analyze_min now correctly passes 'self' as the first argument
        self.game = game.match_id
        
        try:
            gold_diff, level_diff, cs_diff, cspm_diff, gpm_diff, avg_gold_diff, cspmxd, gpmxd = self.analyze_min(minute, game)
        except:
            gold_diff, level_diff, cs_diff, cspm_diff, gpm_diff, avg_gold_diff, cspmxd, gpmxd = 0,0,0,0, 0,0,0,0
        
        self.gold_diff = gold_diff
        self.level_diff = level_diff
        self.cs_diff = cs_diff
        self.cspm_diff = cspm_diff
        self.gpm_diff = gpm_diff
        self.avg_gold_diff = avg_gold_diff
        self.cspm = cspmxd
        self.gpm = gpmxd

    def __str__(self):
        return f'gold diff: {self.gold_diff},cs diff: {self.cs_diff}'

    def to_dict(self):
        return {
            "gold_difference" : self.gold_diff,
            "level_difference" : self.level_diff,
            "cs_diff" : self.cspm_diff,
            "cspm" : self.cspm,
            "avg_gold_diff": self.avg_gold_diff
        }





    def analyze_min(self, minute, game):  # Added 'self' to correctly define this as an instance method

        if minute > len(game.timelineDto['info']['frames']):
            return 0,0,0,0,0,0

        def find_id(puuid):
            for i in game.timelineDto['info']['participants']:
                if i['puuid'] == puuid:
                    return i['participantId']

        myPuuid = game.me['puuid']
        lanerPuuid = game.laner['puuid']
        pid = str(find_id(myPuuid))
        laner_pid = str(find_id(lanerPuuid))

        my_stats_at_min = game.timelineDto['info']['frames'][minute]['participantFrames'][pid]
        laner_stats_at_min = game.timelineDto['info']['frames'][minute]['participantFrames'][laner_pid]

        total_game_gold = 0
        for i in range(1,11):
            if str(i) == pid or str(i) == laner_pid: continue
            stats = game.timelineDto['info']['frames'][minute]['participantFrames'][str(i)]
            total_game_gold += stats['totalGold']
        average_gold = total_game_gold / 8 if total_game_gold else 0
        
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

        avg_gold_diff = totalGold - average_gold

        return (gold_diff, level_diff, cs_diff, cspm_diff, gpm_diff, avg_gold_diff, cspm, gpm)



    


        