import requests
import urllib
import json

from setup import *
import db as db

import numpy as np
import matplotlib.pyplot as plt
import statistics as st
from collections import Counter
from scipy.stats import norm

#import analysis
from operator import itemgetter




#   the development is not going well
#   print basic stats and 10 min basic stats properlu






# my,enemy = get_teams_advanced(match_id,puuid,False)
# myTop, myJungle, myMid, myAdc, mySupp = my
# enemyTop, enemyJungle, enemyMid, enemyAdc, enemySupp = enemy

champ: itemgetter = itemgetter('championName')

# reporting
def tierlist(minimum_games):

    S, A, B, C, D, F = [], [], [], [], [], []

    champs = db.open_db()
    for champ in champs['champs']:
        wr = champ['winrate']
        name = champ['name']
        total = champ['total']
        if total >= minimum_games:
            if wr <= 0.45:                   F.append(name)
            elif wr > 0.45 and wr <=  0.50 : D.append(name)
            elif wr > 0.50 and wr <=  0.55 : C.append(name)
            elif wr > 0.55 and wr <=  0.60 : B.append(name)
            elif wr > 0.60 and wr <=  0.70 : A.append(name)
            elif wr > 0.70                 : S.append(name)

    print(f'S:\t{S}\n\nA:\t{A}\n\nB:\t{B}\n\nC:\t{C}\n\nD:\t{D}\n\nF:\t{F}\n\n')

def bulk_on_matchDto(count,func):
    matches = get_recent_matches(myPuuid,count)
    for i in range(0,count):
        match = matches[i]
        try:
            func(match)
        except:
            continue


def main():
    

    ag = get_puuid('Tryndamere','L9 FF')


    recent = get_recent_matches(ag,30)
    #for i in recent:
    #    analysis.analyze_game_end(i,ag)
    for i in recent:
        parts = get_participants(i)
        for part in parts:
            #print(part['championName'])
            print(champ(part))
 

main()