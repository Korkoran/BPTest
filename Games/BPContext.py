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

log = None
concepts = None

strileckaConcepts = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
robotiConcepts = [1, 2, 3, 4, 5, 6]
tetrisConcepts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def tetris():
    print len(logs_tetris.user.unique())
    print len(logs_tetris)
    users = logs_tetris.user.unique()
    out =[]
    for user in users:
        tmp = logs_tetris.loc[logs_tetris['user']==user]
        out.append(len(tmp))
    print np.mean(out)
    print np.median(out)
# tetris()
def roboti():
    print len(logs_roboti.user.unique())
    print len(logs_roboti)
    users = logs_roboti.user.unique()
    out =[]
    for user in users:
        tmp = logs_roboti.loc[logs_roboti['user']==user]
        out.append(len(tmp))
    print np.mean(out)
    print np.median(out)
# roboti()
def strilecka():
    print len(logs_strilecka.user.unique())
    print len(logs_strilecka)
    users = logs_strilecka.user.unique()
    out =[]
    for user in users:
        tmp = logs_strilecka.loc[logs_strilecka['user']==user]
        out.append(len(tmp))
    print np.mean(out)
    print np.median(out)
# strilecka()

casy = logs_roboti[(logs_roboti['success']==1) & (logs_roboti['mistakes'] < 10)].gameLength.tolist()

concepty = Util.tetris_level.concept.unique()
print concepty
class level:
    id = None
    concept = None
    median_time = None
    median_mistakes = None
out = []
for concept in concepty:
    levely = Util.roboti_level.loc[Util.roboti_level['concept'] == concept, 'level'].tolist()
    for lvl in levely:
        tmp = Util.roboti_session_log.loc[(Util.roboti_session_log['robotConcept'] == concept) & (Util.roboti_session_log['level'] == lvl)]
        d = level()
        d.concept = concept
        d.id = lvl
        d.median_time = np.median(tmp.gameLength.tolist())
        d.median_mistakes = np.mean(tmp.mistakes.tolist())
        out.append(d)

casy.sort()
print len(casy)
#print casy
i = 0
while casy[i] < 3000:
    i += 1
del casy[:i]
median = np.median(casy)
#print casy
first = 0
second = 0
third = 0
forth = 0
user_out =[]
users = logs_roboti.user.unique()
for user in users:
    local_log = logs_roboti[(logs_roboti['user'] == user) & (logs_roboti['success'] == 1)]
    hodnoceni = 0
    mistake = 0
    for index, row in local_log.iterrows():
        t = row['gameLength']
        l = row['level']
        c = row['robotConcept']
        m = row['mistakes']
        match = [x for x in out if x.id == l and x.concept == c]
        if t > match[0].median_time:
            hodnoceni -=1
        else:
            hodnoceni +=1
        if m > match[0].median_mistakes:
            mistake -=1
        else:
            mistake +=1
    if hodnoceni > 0 and mistake > 0:
        first +=1
    if hodnoceni > 0 and mistake < 0:
        second +=1
    if hodnoceni <0 and mistake >0:
        third +=1
    if hodnoceni < 0 and mistake < 0:
        forth +=1
    user_out.append((user, hodnoceni, mistake))
    plt.plot(hodnoceni,mistake,'ro')
    if hodnoceni > 10 and mistake > 10:
        pass

# PROvest neco s grafem
# plt.show()
print user_out
print
print first
print second
print third
print forth