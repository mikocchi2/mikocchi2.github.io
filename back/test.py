from game import Game
from setup import *
from colorama import init, Fore, Style

puuid = get_puuid('Mikky','3030')
games = Game.recent_games(puuid,20)
init(autoreset=True)

print("sexs")
"""
for game in games:
    try:
        matchup = game.matchup
        if game.min15 is None: continue
        grade = game.gold_difference_grade()
        geade_str = str(grade)
        gold_diff = game.min15.gold_diff
        gds = str(gold_diff)

        grade2 = game.gold_difference_grade_avg()
        geade_str2 = str(grade2)
        gold_diff2 = game.min15.avg_gold_diff
        gds2 = str(gold_diff2)

        strr = f'{geade_str}   {geade_str2}    {matchup:20}     {gds:10}   {gds2:10}'

        if grade in [0,1,2]:     print(Fore.RED + Style.BRIGHT +   strr)
        elif grade in [3,4]:     print(Fore.RED +                  strr)
        elif grade == 5:         print(Fore.YELLOW +               strr)
        elif grade in [6,7]:     print(Fore.YELLOW + Style.BRIGHT + strr)
        elif grade == 8   :       print(Fore.GREEN + geade_str + strr)
        elif grade in [9,10]:    print(Fore.GREEN + Style.BRIGHT + strr)

    


    except Exception as e:
        print(e)
        continue
"""
for game in games:
    print(game.to_dict())