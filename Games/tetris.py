import Util
import matplotlib.pyplot as plt
import numpy
import Test.Util as test_Util
import matplotlib.patches as mpatches
import math
from collections import OrderedDict
from operator import itemgetter
import scipy.stats as st
import pandas as pd
from datetime import datetime
from enum import Enum
from matplotlib_venn import venn3

logs_strilecka = Util.strilecka_session_log
logs_roboti = Util.roboti_session_log
logs_tetris = Util.tetris_session_log
tetris_level = Util.tetris_level
concepts = tetris_level.concept.unique()

def firstLevelLossers(concept):
    u = 0

    log = logs_tetris.loc[(logs_tetris['concept']==concept) & (logs_tetris['level'] == 1)]
    users = log.user.unique()
    for user in users:

        local = log.loc[(log['user'] == user), 'success'].tolist()
        if 1 not in local:
            u += 1
    return u

def four_five_levels():
    four_five_concpets = []
    for conc in concepts:
        if len(tetris_level.loc[tetris_level['concept'] == conc]) <=5:
            four_five_concpets.append(conc)
    for f in four_five_concpets:
        tmp = logs_tetris.loc[logs_tetris['concept'] == f]
        fll = firstLevelLossers(f)
        print fll
        levels = tetris_level.loc[tetris_level['concept'] == f, 'level'].tolist()
        out =[]
        for lvl in levels:
            out.append(tmp.loc[tmp['level'] == lvl, 'success'].tolist().count(1))
        print out
        maxim = fll + out[0]
        out2 = []
        for f in out:
            out2.append(f/float(maxim))
        plt.plot(out2)
    numConcept = [1,2,3,4,5]

    plt.grid(True)
    plt.xticks(range(0,5), numConcept)
    plt.show()
four_five_levels()