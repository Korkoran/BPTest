import Util
import matplotlib.pyplot as plt

logsStrilecka = Util.strilecka_session_log
logsRoboti = Util.roboti_session_log
logsTetris = Util.tetris_session_log

strileckaConcepts = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11]
robotiConcepts = [1,2,3,4,5,6]
tetrisConcepts = [1,2,3,4,5,6,7,8,9,10]

def survivors(game):
    sur = [0]* 8
    restart = [0]*8
    levels = [1,2,3,4,5,6,7]
    for level in levels:
        if game == "strilecka":
            sur[level] = logsStrilecka.loc[logsStrilecka['level']==level, "success"].tolist().count(1)
            restart[level] = logsStrilecka.loc[logsStrilecka['level']==level, "success"].tolist().count(0)
        elif game == "tetris":
            sur[level] = logsTetris.loc[logsTetris['level']==level, "success"].tolist().count(1)
            restart[level] = logsTetris.loc[logsTetris['level']==level, "success"].tolist().count(0)
        elif game == "roboti":
            sur[level] = logsRoboti.loc[logsRoboti['level']==level, "success"].tolist().count(1)
            restart[level] = logsRoboti.loc[logsRoboti['level']==level, "success"].tolist().count(0)
        else:
            print "Unknown game"
    print restart[1:]
    print sur[1:]


#oblibenost conceptu, nepoci s pridanim konceptu pocita vsechny dohromady
def favConcepts(game):
    if game == "strilecka":
        for concept in strileckaConcepts:
            print len(logsStrilecka.loc[logsStrilecka['concept']== concept])
    elif game == "tetris":
        for concept in tetrisConcepts:
            print len(logsTetris.loc[logsTetris['concept']== concept])
    elif game == "roboti":
        for concept in robotiConcepts:
            print len(logsRoboti.loc[logsRoboti['robotConcept']== concept])
    else:
        print "Unknown game"




#prumerne chyby pro kazdy koncept
#strilecka ma max 3 naboje
def conceptMistakes(game):
    if game == "strilecka":
        for concept in strileckaConcepts:
            tmp =logsStrilecka.loc[logsStrilecka['concept']== concept, 'mistakes'].tolist()
            sumMistakes = sum(tmp)
            length = len(tmp)
            if length !=0:
                avg = sumMistakes/float(length)
                print avg

    elif game == "roboti":
        for concept in robotiConcepts:
            tmp =logsRoboti.loc[logsRoboti['robotConcept']== concept, 'mistakes'].tolist()
            sumMistakes = sum(tmp)
            length = len(tmp)
            if length !=0:
                avg = sumMistakes/float(length)
                print avg
            else:
                print 0

    elif game == "tetris":
        for concept in tetrisConcepts:
            tmp =logsTetris.loc[logsTetris['concept']== concept, 'mistakes'].tolist()
            sumMistakes = sum(tmp)
            length = len(tmp)
            if length !=0:
                avg = sumMistakes/float(length)
                print avg

    else:
        print "Unknown game"

def tryNextLevel(game):
    pass

#kolik lidi se nedostalo pres prvni level
users = logsRoboti.user.unique()
u = 0
for user in users:
    tmp= logsRoboti.loc[(logsRoboti['user']==user) & (logsRoboti['level'] == 1)]
    #print tmp

    userConcepts = tmp.robotConcept.unique()
    for c in userConcepts:
        local = tmp.loc[(tmp['robotConcept']== c), 'success'].tolist()
        #print local
        if 1 not in local:
            u += 1

print u

#o kolik se zlepsili uzivatele pri druhem a dalsim pokusu
def loweringMistakes():
    pass


loweringMistakes()

#porovna chyby na stejnych levech v ruznych konceptech
def sameLevelMistakes():
    pass


#conceptMistakes("strilecka")
#favConcepts("roboti")
#survivors("strilecka")
#tryNextLevel("strilecka")