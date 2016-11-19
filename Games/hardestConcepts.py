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

log = None
concepts = None

strileckaConcepts = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
robotiConcepts = [1, 2, 3, 4, 5, 6]
tetrisConcepts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# otestuje jestli hra existuje, nastavi globalni promenne log a concepts
def test_game_name(game):
    global log
    global concepts
    if game == "tetris":
        log = logs_tetris
        concepts = tetrisConcepts
    elif game == "strilecka":
        log = logs_strilecka
        concepts = strileckaConcepts
    elif game == "roboti":
        log = logs_roboti
        concepts = robotiConcepts
    else:
        raise ValueError("Unknown game, use of one {'tetris', 'strilecka', 'roboti'}")

def most_favourite_concepts(game, graf):
    test_game_name(game)
    out = []
    for concept in concepts:
        num =0
        #pozor na roboConcepty
        if game == "roboti":
            tmp = log.loc[log['robotConcept'] == concept]
        else:
            tmp = log.loc[log['concept'] == concept]
        num = len(tmp)
        out.append(num)
    if graf:
        plt.bar(concepts,out, align = 'center')
        plt.grid(True)
        plt.title(game.capitalize())
        plt.xlabel("Koncepty")
        plt.ylabel("Pocet odpovedi")
        plt.xticks(concepts)
        plt.show()
    else:
        return out
# most_favourite_concepts("tetris", True)

def hardest_concepts(game):
    test_game_name(game)

    out = []
    err = []
    for concept in concepts:
        if game == "roboti":
            tmp = log.loc[log['robotConcept'] == concept]
        else:
            tmp = log.loc[log['concept'] == concept]
        errors =sum(tmp.mistakes.tolist())
        num = len(tmp)
        out.append(errors/float(num))
        err.append(test_Util.proportionConfidenceInterval(errors, num)[0])

    print err
    plt.bar(concepts, out, align = 'center', color = 'red', yerr = err)
    plt.xlabel("koncepty")
    plt.ylabel("obtiznost")
    plt.grid(True)
    plt.title(game.capitalize())
    plt.show()

#hardest_concepts("tetris")

def too_many_mistakes(game):
    log = Util.tetris_session_log
    n =(log.loc[(log['mistakes'] > 15) & (log['success']==1)])
    print len(n.user.unique())
too_many_mistakes("roboti")