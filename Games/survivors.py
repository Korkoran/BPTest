import Util
import matplotlib.pyplot as plt
import numpy
import math
from collections import OrderedDict
from operator import itemgetter
import scipy.stats as st
import pandas as pd
from enum import Enum

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


# vraci dataframe pro casovou analyzu (bez prilis dlouhych casu)
def logForTime(game):
    test_game_name(game)

    pole = None
    low_time = 0
    high_time = 0

    if game == "strilecka":
        pole = [0] * 62
        low_time = 3000
        high_time = 50000

    elif game == "tetris":
        pole = [0] * 1000
        low_time = 3000
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


# ze stackoverflow - nevim jestli muzu pouzit

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * numpy.array(data)
    n = len(a)
    m, se = numpy.mean(a), st.sem(a)
    print se
    h = se * st.t._ppf((1 + confidence) / 2., n - 1)
    return m, m - h, m + h

# print mean_confidence_interval([10,15,16,20,32,45])


def my_mean_interval(data):
    confidence = 0.95
    array = numpy.array(data)
    n = len(array)
    avg = numpy.mean(array)
    standardError= st.sem(data)
    return avg

# print my_mean_interval([10,15,16,20,32,45])

# kolik lidi se nedostalo pres prvni level


def firstLevelLossers(game):
    users = logs_roboti.user.unique()
    u = 0
    test_game_name(game)

    for user in users:
        tmp = log.loc[(log['user'] == user) & (log['level'] == 1)]
        if game == "roboti":
            userConcepts = tmp.robotConcept.unique()
        else:
            userConcepts = tmp.concept.unique()
        for c in userConcepts:
            if game == "roboti":
                local = tmp.loc[(tmp['robotConcept'] == c), 'success'].tolist()
            else:
                local = tmp.loc[(tmp['concept'] == c), 'success'].tolist()
            if 1 not in local:
                u += 1
    return u


# kolik uzivatelu se dostalo pres levely
# NEDOKONCENE
def survivors(game):
    sur = [0] * 11
    restart = [0] * 11
    levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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

    plt.title(str(game) + " prezivsi")
    plt.plot(sur, '-b')
    plt.plot(restart, '-r')
    plt.xticks(range(0, 10))
    plt.grid(True)
    plt.show()


#survivors("roboti")


# oblibenost conceptu, nepoci s pridanim konceptu pocita vsechny dohromady
# DODELAT zavislost na testgame
def favConcepts(game):
    out = []
    if game == "strilecka":
        for concept in strileckaConcepts:
            out.append(len(logs_strilecka.loc[logs_strilecka['concept'] == concept]))
    elif game == "tetris":
        for concept in tetrisConcepts:
            out.append(len(logs_tetris.loc[logs_tetris['concept'] == concept]))
    elif game == "roboti":
        for concept in robotiConcepts:
            out.append(len(logs_roboti.loc[logs_roboti['robotConcept'] == concept]))
    else:
        raise ValueError("Unknown game")

    plt.bar(range(1, 7), out, align='center')
    plt.xticks(range(1, 7))
    plt.grid(True)
    plt.show()


# favConcepts("roboti")

# prumerne chyby pro kazdy koncept
# strilecka ma max 3 naboje- divne vysledky(chybne odpovedi moc ovlivnuji prumer)
def conceptMistakes(game):
    test_game_name(game)

    all_mistakes = sum(log.mistakes) / float(len(log))

    print "Kompletni prumer: " + str(all_mistakes)

    for concept in concepts:
        if game == "roboti":
            tmp = log.loc[log['robotConcept'] == concept, 'mistakes'].tolist()
            #uprava, koncepty v robotech jsou podkoncepty
        else:
            tmp = log.loc[log['concept'] == concept, 'mistakes'].tolist()
        tmp2 = [i for i in tmp if i < 60]
        sumMistakes = sum(tmp2)
        length = len(tmp2)
        if length != 0:
            avg = sumMistakes / float(length)
            print avg
        else:
            print 0

# conceptMistakes("roboti")


# o kolik se zlepsili uzivatele pri druhem a dalsim pokusu
# nejede - potrebuje moc casu
# log je serazeny sestupne, potreba obratit pole
# podivne vysledky - jeste zkontrolovat - slova se muzou v n opakovat NEDOKONCENE
def loweringMistakes(lower_boundary, higher_boundary):
    if lower_boundary > higher_boundary:
        raise ValueError("higher boundarie is larger than lower")

    local_log = Util.get_roboti_shot_log()
    log = local_log[['user', 'word']]

    lower = 0
    higher = 0
    same_wrong = 0
    same_right = 0
    exactly_two = 0
    exactly_one = 0
    more_than_two = 0

    users = log.user.tolist()
    words = log.word.tolist()
    frame = local_log.loc[lower_boundary: higher_boundary]

    for n in range(lower_boundary, higher_boundary):
        user = users[n]
        word = words[n]
        pole = frame.loc[(frame['user'] == user) & (frame['word'] == word), 'correct'].tolist()[::-1]

        if len(pole) == 1:
            exactly_one += 1
        if len(pole) == 2:
            exactly_two += 1
            if (pole[0] == 1) & (pole[1] == 0):
                lower += 1
            elif (pole[0] == 0) & (pole[1] == 1):
                higher += 1
            elif (pole[0] == 0) & (pole[1] == 0):
                same_wrong += 1
            elif (pole[0] == 1) & (pole[1] == 1):
                same_right += 1
        if len(pole) > 2:
            more_than_two += 1

    print lower
    print higher
    print same_wrong
    print same_right
    print exactly_two
    print exactly_one
    print more_than_two
    # print local_log.loc[(local_log['user']==log.user.tolist[0]) & (local_log['word'] == log.word.tolist()[0])]


# loweringMistakes(150000, 180000)

# porovna chyby na stejnych levech v ruznych konceptech
# nejde ruzne levely maji ruzne rychlosti a frekvence
def sameLevelMistakes():
    pass


# zjisti chybovost ve strilecce kde jsou texty delsi
# max level  = 4 concept 7
def tooLong():
    for concept in strileckaConcepts:
        log = logs_strilecka.loc[logs_strilecka['concept'] == concept]
        levels = Util.strilecka_level.loc[Util.strilecka_level['concept'] == concept, 'level'].tolist()
        level_fail = 0
        print "Koncept cislo:" + str(concept)
        for level in levels:
            level_tries = len(log.loc[log['level'] == level])
            level_fail = log.loc[log['level'] == level, 'success'].tolist().count(0)

            print "level:" + str(level) + ": " + str(level_tries) + ":" + str(level_fail) + " Pomer je: " + str(
                float(level_fail) / (level_tries - level_fail))


# tooLong()

# porovna chybovost v ruznych konceptech ve strilecce.

# porovna ruzne hry, pocet pokusu, prumerny straveny cas na uzivatele
# NEDOKONCENE
def triesPerGame(game):
    test_game_name(game)
    users = log.user.unique()
    log_for_time = logForTime(game)

    allTimes = []
    for user in users:
        allTimes.append(sum(log_for_time.loc[log['user'] == user, 'gameLength'].tolist()))

    return numpy.mean(allTimes), numpy.median(allTimes)


# triesPerGame("tetris")

def number_of_users(game):
    test_game_name(game)

    users = log.user.unique()

    # print len(users) * triesPerGame(game)

    print sum(log.gameLength.tolist())


# number_of_users("strilecka")
# number_of_users("tetris")
# number_of_users("roboti")

# pro kazdou hru zjisti kolik prumerne slov uzivatel procvici
# pro roboty z robot shot log
# pro strilecku z delky levelu (pouze uspesne)
# pro tetris stejne jako pro strilecku
# pocita jenom uspesne pokusy - nejde zjistit kolik slov videl neuspesny uzivatel
def number_of_practiced_words(game):
    test_game_name(game)
    local_log = log.loc[log['success'] == 1]

    if game == "tetris":
        tetris_level_log = Util.tetris_level
        number_of_words = 0

        for index, row in local_log.iterrows():
            tmp = tetris_level_log.loc[(tetris_level_log['concept'] == row['concept']) &
                                       (tetris_level_log['level'] == row['level']), 'words'].tolist()
            string_tmp = ''.join(tmp)

            number_of_words += sum([int(s) for s in string_tmp.split(',') if s.isdigit()])
        print number_of_words
    if game == "strilecka":
        number_of_words = 0
        strilecka_level_log = Util.strilecka_level_word
        strilecka_level = Util.strilecka_level

        for index, row in local_log.iterrows():
            id = strilecka_level.loc[(strilecka_level['concept'] == row['concept']) &
                                     (strilecka_level['level'] == row['level']), 'id'].tolist()[0]
            tmp = len(strilecka_level_log.loc[strilecka_level_log['level'] == id, 'word'].tolist())
            number_of_words += tmp
        print number_of_words

    if game == "roboti":
        pass


# number_of_practiced_words("tetris")

# zjisti nejtezsi slova pro kazdou hru(asi nepujde) - pujde pro roboty
# slova maji jenom cisla
def most_difficult_words():
    local_log = Util.get_roboti_shot_log()
    words = local_log.word.unique()
    wrongs = []

    for word in words:
        wrong = len(local_log.loc[(local_log['word'] == word) & (local_log['correct'] == 0)])
        wrongs.append(wrong)

    d = dict(zip(words, wrongs))
    ordered = OrderedDict(sorted(d.items(), key=itemgetter(1)))
    print ordered


#most_difficult_words()

# porovna hry oproti klasickym diktatum
def compare_games_to_dictates():
    pass

# zjisti kolik lidi vyzkousi vice nez jednu hru
# zkontrolovat vraci prekvapive moc
def try_more_games():
    roboti_users = Util.roboti_session_log.user.unique()
    tetris_users = Util.tetris_session_log.user.unique()
    strilecka_users = Util.strilecka_session_log.user.unique()

    print len(roboti_users)
    print len(tetris_users)
    print len(strilecka_users)
    n1= set(roboti_users).intersection(tetris_users)
    n2= set(tetris_users).intersection(strilecka_users)
    n3 = set(roboti_users).intersection(strilecka_users)

    print n1

    celkem = len(set(n1).intersection(n2))
    print len(n1)
    print len(n2)
    print len(n3)
    print celkem

# try_more_games()

# vypise pole s pocty chyb na indexu
def mistakes_test():
    global log
    log = Util.roboti_session_log
    mistakes = [0]*200

    for index, row in log.iterrows():
        pozice = int(row['mistakes'])
        if pozice >=0:
            mistakes[pozice] +=1

    print mistakes
    values = numpy.array(mistakes)
    searchval = 1
    ii = numpy.where(values == searchval)[0]
    print max(ii)
    plt.plot(mistakes[0:25], 'r-')
    plt.grid(True)
    plt.show()
# mistakes_test()

# pro kazdy level(mozna to pouzit jako skore pro uzivatele)
# vypocita podle nejake rovnice obtiznost levelu,
# vytvori graf a porovna s grafem survivors
def roboti_level_compare():
    pass

# porovna vraceni se ke hre k diktatum
def returning_users(game):
    test_game_name(game)
    maximum = max(log.id.tolist())
    print maximum
    first_third = log.loc[log['id'] < maximum/3, 'user'].unique().tolist()
    second_third = log.loc[log['id'] > maximum - maximum/3, 'user'].unique().tolist()

    first_half = log.loc[log['id'] < maximum/2, 'user'].unique().tolist()
    second_half = log.loc[log['id'] > maximum - maximum/2, 'user'].unique().tolist()
    n1= set(first_third).intersection(second_third)
    n2 = set(first_half).intersection(second_half)

    print len(first_half)
    print len(second_half)
    print len(n2)

    print len(first_third)
    print len(second_third)
    print len(n1)

# returning_users("tetris")

def returning_users(game):
    test_game_name(game)
    start_first = "2016-05-01"
    end_first = "2016-06-01"
    end_second = "2016-07-01"

    first_month_users = log.loc[(log['time'] > pd.Timestamp(start_first)) &
                                (log['time'] < pd.Timestamp(end_first)), 'user'].unique().tolist()
    second_month_users = log.loc[(log['time'] > pd.Timestamp(end_first)) &
                                 (log['time'] < pd.Timestamp(end_second)), 'user'].unique().tolist()

    out = set(first_month_users).intersection(second_month_users)
    print len(first_month_users)
    print len(second_month_users)
    print len(out)
# returning_users("strilecka")

# zjisti kolik uzivatelu odpadne po mesici a kolik novych se jich prida
def more_new_players():
    pass

# stejne jako pro survivors ale ukazuje graf pro kazdy koncept
def survivors_for_concept(game, concept):
    pass

# graf pro chyby v konceptech
# nemuzou se delat vsechny koncepty dohromady - maji ruznou delku
# roboti maji v sobe nekolik konceptu
def level_mistake_chance(game, concept):
    test_game_name(game)

    local_log = log.loc[log['robotConcept'] == concept]

    levels = [1,2,3,4,5,6,7]
    for level in levels:
        level_log = local_log.loc[local_log['level'] == level]


#  level_mistake_chance("roboti",1)

# posledni vec pred opustenim
def xed(game):
    test_game_name(game)

    users = log.user.unique().tolist()
    zeros = 0
    ones = 0
    level = [0]*15

    for user in users:
        local_log = log.loc[log['user'] == user]
        last_id = local_log.id.iget(-1)
        tmp = local_log.loc[local_log['id'] == last_id]
        level[tmp.level.tolist()[0]] +=1
        if tmp.success.tolist()[0] == 1:
            ones += 1
        else:
            zeros += 1
    print zeros
    print ones
    print level # tohle vlastne nic nerika
# xed("strilecka")

def player_types(game):
    test_game_name(game)

    achievers = 0
    explorers = 0
    careless = 0
    lost = 0

    class_levels = []

    class lvl:
        id = 0
        concept = 0
        mistakes = 0
        gameLength = 0

    for concept in concepts:
        l_log = log.loc[log['concept'] == concept]
        levels = Util.tetris_level.loc[Util.tetris_level['concept'] == concept, 'level'].unique().tolist()
        print levels

        #nektere levely nemaji zadny zaznam, median vraci nan
        for level in levels:
            l = lvl()
            level_tmp = l_log.loc[l_log['level'] == level, ['mistakes', 'gameLength']]
            level_avg = numpy.mean(level_tmp.mistakes.tolist())
            level_time = numpy.mean(level_tmp.gameLength.tolist())
            # print level_tmp.mistakes.tolist()
            l.id = level
            l.concept = concept
            l.mistakes = level_avg
            l.gameLength = level_time
            class_levels.append(l)

    users = log.user.unique().tolist()
    for user in users:
        user_error_score = []
        user_time_score = []
        user_log = log.loc[(log['user'] == user) & log['success'] == 1]
        if len(user_log) > 10:
            for index, row in user_log.iterrows():
                c = row['concept']
                l = row['level']
                m = row['mistakes']
                t = row['gameLength']
                # nejakou lepsi strukturu na vyhledavani
                for class_level in class_levels:
                    if class_level.id == l & class_level.concept == c:
                        #mozne predelat, podle skutecne obtiznosti
                        #upravit to co pridavam to pole (1, -1)
                        if class_level.mistakes >= m:
                            user_error_score.append(1)
                        elif class_level.mistakes < m:
                            user_error_score.append(-1)
                        if class_level.gameLength >= t:
                            user_time_score.append(1)
                        elif class_level.gameLength < t:
                            user_time_score.append(-1)
                    else:
                        continue
            # print "errors: " + str(sum(user_error_score))
            # print "time: " + str(sum(user_time_score))
            if sum(user_error_score) > 0 and sum(user_time_score ) > 0:
                achievers += 1
            if sum(user_error_score) > 0 and sum(user_time_score) < 0:
                explorers += 1
            if sum(user_error_score) < 0 and sum(user_time_score) > 0:
                careless += 1
            if sum(user_error_score) < 0 and sum(user_time_score) < 0:
                lost += 1

    print achievers
    print explorers
    print careless
    print lost
# player_types("strilecka")

