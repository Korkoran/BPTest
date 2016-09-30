import Util
import matplotlib.pyplot as plt
import numpy
#import scipy.stats as st

logs_strilecka = Util.strilecka_session_log
logs_roboti = Util.roboti_session_log
logs_tetris = Util.tetris_session_log

log = None
concepts = None

strileckaConcepts = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
robotiConcepts = [1, 2, 3, 4, 5, 6]
tetrisConcepts = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#otestuje jestli hra existuje, nastavi globalni promenne log a concepts
def testGameName(game):
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
        raise ValueError("Unknown game")

# vraci dataframe pro casovou analyzu (bez prilis dlouhych casu)
def logForTime(game):
    testGameName(game)

    pole = None
    low_time = 0
    high_time = 0

    if game == "strilecka":
        pole = [0] * 62
        low_time = 3000
        high_time = 50000

    elif game == "tetris":
        pole = [0] * 1000
        low_time = 1000
        high_time = 230000

    elif game == "roboti":
        pole = [0] * 150
        low_time = 3000
        high_time = 60000

    game_lengths = log.gameLength.tolist()
    for length in game_lengths:
        position = length / 1000 + 1
        pole[position] += 1

    # print pole
    # plt.plot(pole)
    # plt.show()

    return log.loc[(log['gameLength'] > low_time) & (log['gameLength'] < high_time)]


#kolik lidi se nedostalo pres prvni level
def firstLevelLossers(game):
    users = logs_roboti.user.unique()
    u = 0
    testGameName(game)

    for user in users:
        tmp= log.loc[(log['user']==user) & (log['level'] == 1)]
        if game == "roboti":
            userConcepts = tmp.robotConcept.unique()
        else:
            userConcepts = tmp.concept.unique()
        for c in userConcepts:
            if game == "roboti":
                local = tmp.loc[(tmp['robotConcept']==c), 'success'].tolist()
            else:
                local = tmp.loc[(tmp['concept']== c), 'success'].tolist()
            if 1 not in local:
                u += 1
    return u

#kolik uzivatelu se dostalo pres levely
#NEDOKONCENE
def survivors(game):
    sur = [0]* 11
    restart = [0]*11
    levels = [1,2,3,4,5,6,7,8,9,10]

    for level in levels:
        if game == "strilecka":
            sur[level] = logs_strilecka.loc[logs_strilecka['level'] == level, "success"].tolist().count(1)
            restart[level] = logs_strilecka.loc[logs_strilecka['level'] == level, "success"].tolist().count(0)
        elif game == "tetris":
            sur[level] = logs_tetris.loc[logs_tetris['level'] == level, "success"].tolist().count(1)
            restart[level] = logs_tetris.loc[logs_tetris['level'] == level, "success"].tolist().count(0)
        elif game == "roboti":
            sur[level] = logs_roboti.loc[logs_roboti['level'] == level, "success"].tolist().count(1)
            restart[level] = logs_roboti.loc[logs_roboti['level'] == level, "success"].tolist().count(0)
        else:
            raise ValueError("Unknown game")

    sur[0] = sur[1] + firstLevelLossers(game)
    print restart[1:]
    print sur
    plt.plot(sur, '-b')
    plt.plot(restart, '-r')
    plt.xticks(range(0,10))
    plt.grid(True)
    plt.show()

#survivors("strilecka")

#oblibenost conceptu, nepoci s pridanim konceptu pocita vsechny dohromady
def favConcepts(game):
    if game == "strilecka":
        for concept in strileckaConcepts:
            print len(logs_strilecka.loc[logs_strilecka['concept'] == concept])
    elif game == "tetris":
        for concept in tetrisConcepts:
            print len(logs_tetris.loc[logs_tetris['concept'] == concept])
    elif game == "roboti":
        for concept in robotiConcepts:
            print len(logs_roboti.loc[logs_roboti['robotConcept'] == concept])
    else:
        raise ValueError("Unknown game")

#favConcepts("strilecka")

#prumerne chyby pro kazdy koncept
#strilecka ma max 3 naboje
def conceptMistakes(game):
    testGameName(game)

    for concept in concepts:
        if game == "roboti":
            tmp = log.loc[log['robotConcept'] == concept, 'mistakes'].tolist()
        else:
            tmp =log.loc[log['concept']== concept, 'mistakes'].tolist()
        sumMistakes = sum(tmp)
        length = len(tmp)
        if length !=0:
            avg = sumMistakes/float(length)
            print avg
        else:
            print 0

#conceptMistakes("roboti")
def tryNextLevel(game):
    pass

#firstLevelLossers("strilecka")

#o kolik se zlepsili uzivatele pri druhem a dalsim pokusu
def loweringMistakes():
    pass

loweringMistakes()

#porovna chyby na stejnych levech v ruznych konceptech
def sameLevelMistakes():
    pass

#zjisti chybovost ve strilecce kde jsou texty delsi
#max level  = 4 concept 7
def tooLong():
    for concept in strileckaConcepts:
        log = logs_strilecka.loc[logs_strilecka['concept'] == concept]
        levels = Util.strilecka_level.loc[Util.strilecka_level['concept'] == concept, 'level'].tolist()
        level_fail = 0
        print "Koncept cislo:" + str(concept)
        for level in levels:
            level_tries = len(log.loc[log['level'] == level])
            level_fail = log.loc[log['level'] == level, 'success'].tolist().count(0)

            print "level:" + str(level) + ": " + str(level_tries) + ":" + str(level_fail) + " Pomer je: " + str(float(level_fail)/(level_tries-level_fail))
tooLong()
#porovna chybovost v ruznych konceptech ve strilecce.



#porovna ruzne hry, pocet pokusu, prumerny straveny cas na uzivatele
#NEDOKONCENE
def triesPerGame(game):

    testGameName(game)
    users = log.user.unique()
    log_for_time = logForTime(game)

    allTimes = []
    for user in users:
        allTimes.append(sum(log_for_time.loc[log['user'] == user, 'gameLength'].tolist()))

    return numpy.mean(allTimes)

#triesPerGame("roboti")


#print log.head()
#print logForTime("roboti")
#conceptMistakes("strilecka")
#favConcepts("roboti")
#survivors("strilecka")
#tryNextLevel("strilecka")