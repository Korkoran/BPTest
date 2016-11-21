import Test.Util as test_Util
import Util
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import math
import numpy as np
from collections import OrderedDict
from operator import itemgetter
import scipy.stats as st
import pandas as pd
from datetime import datetime
from enum import Enum
from matplotlib_venn import venn3

'''
z logu nejde vycist jak hra vypada (jestli uzivatel zaplnil nektery sloupec tak, ze nesel dokoncit nebo
skladal slova tak aby level dokoncil - mene slov nez mista) - doporucit tolik rad aby tohle neslo udelat
u tetrisu generovat slova doprostred ne nahodne, nelze zjistit v jakem vzoru dela uzivatel chyby
umoznit uzivatelum pokracovat v tom levelu kde skoncili
vyradit z logu radky kde je moc chyb - roboti 20+
'''
logs_strilecka = Util.strilecka_session_log
logs_roboti = Util.roboti_session_log
logs_tetris = Util.tetris_session_log
level_strilecka = Util.strilecka_level
level_roboti = Util.roboti_level
level_tetris = Util.tetris_level

log = None
level_log = None
concepts = None

strileckaConcepts = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
robotiConcepts = [1, 2, 3, 4, 5, 6]
tetrisConcepts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def test_game_name(game):
    global log
    global concepts
    global level_log

    if game == "tetris":
        log = logs_tetris
        concepts = tetrisConcepts
        level_log = level_tetris

    elif game == "strilecka":
        log = logs_strilecka
        concepts = strileckaConcepts
        level_log = level_strilecka

    elif game == "roboti":
        log = logs_roboti
        concepts = robotiConcepts
        level_log = level_roboti
    else:
        raise ValueError("Unknown game, use one of {'tetris', 'strilecka', 'roboti'}")


# vraci dataframe pro casovou analyzu (bez prilis dlouhych casu)
def logForTime(game):
    test_game_name(game)

    pole = None
    low_time = 0
    high_time = 0

    if game == "strilecka":
        pole = [0] * 62
        low_time = 3000
        high_time = 1000000

    elif game == "tetris":
        pole = [0] * 1000
        high_time = 180000
        low_time = 3000

    elif game == "roboti":
        pole = [0] * 150
        high_time = 1000000
        low_time = 3000


    # print pole
    # plt.plot(pole)
    # plt.show()

    log.loc[log.gameLength > high_time, 'gameLength'] = high_time
    log.loc[log.gameLength < low_time, 'gameLength'] = low_time
    #log.loc[log.gameLength < low_time, 'gameLength'] = low_time
    return log
    #return log.loc[(log['gameLength'] > low_time) & (log['gameLength'] < high_time)]

def gaming_roles(game,category):
    all_log = logForTime(game)
    log = logForTime(game)
    log = log[(log['success'] == 1) & (log['mistakes'] < 20)]
    class level:
        id = None
        concept = None
        median_time = None
        median_mistakes = None
        median_repeats = None
    level_array = []
    for concept in concepts:

        for lvl in level_log[level_log['concept'] == concept].level.unique():

            if game == "roboti":
                tmp = log.loc[(log['robotConcept'] == concept) & (log['level'] == lvl)]
                tmp2 = all_log[(all_log['robotConcept'] == concept) & (all_log['level'] == lvl)]
            else:
                tmp = log.loc[(log['concept'] == concept) & (log['level'] == lvl)]
                tmp2 = all_log[(all_log['concept'] == concept) & (all_log['level'] == lvl)]
            d = level()
            bad = len(tmp2[tmp2['success'] ==0])
            good = len(tmp2[tmp2['success'] ==1])
            d.concept = concept
            d.id = lvl
            d.median_time = np.median(tmp.gameLength.tolist())
            d.median_mistakes = np.median(tmp.mistakes.tolist())
            try:
                d.median_repeats = round(float(bad) / good,0)
            except:
                print d.concept,d.id
            level_array.append(d)

    print level_array[6].median_repeats
    first = []
    second = []
    third = []
    forth = []
    #test_game_name(game)
    log = logs_roboti
    users = log.user.unique()

    for user in users:

        local_log = log[(log['user'] == user)]
        if len(local_log) < 5:
            continue
        score_mistake = 0
        score_length = 0
        '''
        tmp_concepts = local_log.concept.unique()
        for con in tmp_concepts:
            if game == "roboti":
                tmp = local_log[local_log['robotConcept'] == con]
            else:
                tmp = local_log[local_log['concept'] == con]
            levels = tmp.level.unique()
            try:
                if game == "roboti":
                    concept_max = max(level_log[level_log['robotConcept'] == con].level.unique())
                else:
                    concept_max = max(level_log[level_log['concept'] == con].level.unique())
            except:
                print con
            for level in levels:
                if level <=0 or concept <=0 or level > concept_max:
                    continue
                tmp2 = tmp[tmp['level'] == level]
                times = tmp2.gameLength.tolist()
                mistakes = tmp2.mistakes.tolist()
                match = [x for x in level_array if x.id == level and x.concept == concept]
                for i in range(len(mistakes)):
                    try:
                        if times[i] > match[0].median_time:
                            score_length -= 1
                            #score_length -= match[0].median_time
                        else:
                            score_length += 1
                            #score_length += match[0].median_time
                        if mistakes[i] > match[0].median_mistakes:
                            score_mistake -= 1
                            #score_mistake -= match[0].median_mistakes
                        else:
                            score_mistake += 1
                            #score_mistake += match[0].median_mistakes
                    except:
                        print (level, concept, concept_max)
        '''
        level_max = max(level_log.level.unique())
        matrix = [[0 for x in range(level_max+1)] for y in range(max(concepts))]

        for index, row in local_log.iterrows():
            t = row['gameLength']
            l = row['level']
            if game == "roboti":
                c = row['robotConcept']
            else:
                c = row['concept']
            m = row['mistakes']
            s = row['success']
            try:
                concept_max = max(level_log[level_log['concept'] == c].level.unique())
            except:
                print l, c
            #predelat podminku nekam jinam nejak lip
            if l <= 0 or c <= 0 or l > concept_max:
                continue
            if s == 0:
                try:
                    matrix[c-1][l-1] +=1
                except:
                    print l, c
                    raise ValueError

            match = [x for x in level_array if x.id == l and x.concept == c]
            try:
                if t > match[0].median_time:
                    score_length -= 1
                    #score_length -= match[0].median_time
                else:
                    score_length += 1
                    #score_length += match[0].median_time
                if m > match[0].median_mistakes:
                    score_mistake -= 1
                    #score_mistake -= match[0].median_mistakes
                else:
                    score_mistake += 1
                    #score_mistake += match[0].median_mistakes
            except:
                print (l, c, concept_max)
        #matrix[5][0] = 5 sesta matice na prvni pozici

        for i in range(max(concepts)):
            for j in range(level_max+1):
                match = [x for x in level_array if x.id == j+1 and x.concept == i+1]
                if len(match) > 0:
                    if match[0].median_repeats == None:
                        continue
                    while matrix[i][j] > match[0].median_repeats:
                        # print match[0].id,match[0].median_repeats, matrix[i][j]
                        score_mistake -= 1
                        score_length -= 1
                        matrix[i][j] -= 1
        if score_length > 0 and score_mistake > 0:
            first.append((user, score_length, score_mistake))
        if score_length > 0 and score_mistake < 0:
            second.append((user, score_length, score_mistake))
        if score_length < 0 and score_mistake > 0:
            third.append((user, score_length, score_mistake))
        if score_length < 0 and score_mistake < 0:
            forth.append((user, score_length, score_mistake))
        plt.plot(score_mistake, score_length, 'ro')
        #print "Done"
    print len(first)
    print len(second)
    print len(third)
    print len(forth)
    # plt.show()

    if category == 1:
        return first
    if category ==2:
        return second
    if category == 3:
        return third
    if category == 4:
        return forth
#gaming_roles("roboti",1)
print
gaming_roles("roboti", 1)
print
#gaming_roles("strilecka", 1)
def different_roles(game, category):
    users = gaming_roles(game, category)
    all_times = []
    for user in users:
        local_log = log[log['user'] == user[0]]
        time = sum(local_log.gameLength.tolist())
        time = time / len(local_log)
        all_times.append(time)
    print np.mean(all_times)

'''different_roles("tetris",1)
different_roles("tetris",2)
different_roles("tetris",3)
different_roles("tetris",4)'''