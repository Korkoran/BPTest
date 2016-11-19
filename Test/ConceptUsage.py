import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import Util
import copy

numConcept = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
session = Util.dictateSession
concepts = Util.getAllConcepts()

'''
zjisti jake procento diktatu uzivatel vyzkousi v jakem konceptu - jake koncepty je treba rozsirit
zjisti kolik procent uzivatelu vyzkouselo vsechny diktaty v konceptu
'''
def conceptUsage():

    arrays = [[] for i in range(max(concept.id for concept in concepts)+1)]
    complete = [0]* 26
    conceptList = []
    class localConcept:
        id = None
        completePr = None
        avarageUse = None
        popularity = None
        realName = None

    for concept in concepts:

        tmp = session.loc[session['concept'] == concept.id]
        uzivatele = tmp.user.unique()
        number_of_dictates = len(concept.dictates)


        for user in uzivatele:
            divided = len(tmp.loc[tmp['user']== user, 'dictate'].unique()) / float(number_of_dictates)
            arrays[concept.id].append(divided)

    for i in range(len(arrays)):
        conc = localConcept()
        length = len(arrays[i])
        for j in arrays[i]:
            if j == 1:
               complete[i] +=1
        if length!=0:
            arrays[i] = (sum(arrays[i]) / float(length)) *100
            complete[i] = (complete[i] / float(length)) *100
            conc.avarageUse = arrays[i]
            conc.completePr = complete[i]
        else:
            arrays[i] = 0
            conc.avarageUse=0
            conc.completePr=0
        #complete[i] = complete[i] / length
        conceptList.append(conc)


    for i in range (len(numConcept)):
        conceptList[i].id = numConcept[i]
        conceptList[i].popularity = Util.conceptPopularity(conceptList[i].id)
    result = dict(zip(range(0,26), arrays))

    plt.bar(numConcept, arrays, align='center')
    plt.xticks(range(0,26), range(0,26))
    plt.xlabel('Koncepty')
    plt.bar(numConcept, complete, color = 'g', align='center')
    plt.title('Procentualni vyjadreni vyuziti diktatu v konceptech')

    blue = mpatches.Patch(color= 'blue', label = 'Procento vyzkousenych diktatu')
    green = mpatches.Patch(color= 'green', label = 'Vsechny diktaty')

    plt.legend(handles = [blue, green])

    plt.axis([0, 26, 0, 90])
    plt.show()

    #na prvni pozici je 0
    conceptList.pop(0)
    return conceptList
# conceptUsage()
'''
Zjisti v jakem konceptu travi uzivatele nejvic casu, s ohledem na ruzne delky diktatu (podle casu na odpoved)

'''
# mohl bych udelat maly graf pro kazdy koncept a diktat a jako yerr pouzit nejmensi a nejvetsi hodnotu
def game_length_per_concept():

    gameLengthPerConcept = []
    err = []
    for concept in concepts:
        conceptTmp = []
        for diktat in concept.dictates:
            tmp = session.loc[session['dictate'] == diktat.id, 'gameLength'].tolist()
            for i in range(len(tmp)):
                if tmp[i] > 300000:
                    tmp[i] = 300000
            neco = sum(tmp)/len(tmp)
            #print 'diktat cislo: ' + str(diktat.id) + ' game Length: '+ str(neco) + ' cas na odpoved: ' + str(neco/len(diktat.answers))
            conceptTmp.append(neco/len(diktat.answers))
        length = len(conceptTmp)
        err.append(Util.mean_confidence_interval(conceptTmp))

        conceptTmp = sum(conceptTmp) / length
        print conceptTmp
        gameLengthPerConcept.append(conceptTmp/float(1000))

    print err

    err2 = []
    for e in err:
        err2.append((e[0] - e[1]) /1000)
    print err2
    plt.xticks(Util.numConcept, Util.STRCONCEPTS)
    plt.grid(True)
    # zkusit dodelat yerr
    #plt.title('Prumerny pocet sekund na jednu odpoved')
    plt.xlabel('koncept')
    plt.ylabel('pocet sekund')
    plt.bar(Util.numConcept,
            gameLengthPerConcept,
            align='center',
            yerr = err2,
            #yerr = [1,1,1,1,0,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
            color='g')
    plt.show()
game_length_per_concept()

def words_with_most_mistakes():
    diktaty = Util.getAllDictates()
    for diktat in diktaty:
        vyplneni = session.loc[session['dictate'] == diktat.id, 'answers'].tolist()
        bezNan = [x for x in vyplneni if not isinstance(x,float)]
        pole = [0] * (len(diktat.answers))
        for s in bezNan:
            polePozic = [position for position, item in enumerate(s) if item == '0']
            for p in polePozic:
                if p < len(pole):
                    pole[p] +=1
        print pole
        if diktat.id == 116:
            prumer = sum(pole)/ len(pole)
            for x in pole:
                if x>prumer*2:
                    print x

words_with_most_mistakes()
#conceptUsage()
#game_length_per_concept()
''''
words_with_most_mistakes()

print list('111001')
for p,i in enumerate(['1','0', '0', '1']):
    if i == '0':
        print p
ctverka = Util.getDictat(110)
vsechni = session.loc[session['dictate'] == ctverka.id, 'answers'].tolist()
bezNan = [x for x in vsechni if not isinstance(x,float)]
print bezNan

pole = [0] * len(ctverka.answers)
print pole
for s in bezNan:
    pozice = [position for position, item in enumerate(s) if item == '0']
    for p in pozice:
        pole[p] +=1
    #print pozice
print pole
print ctverka.answers[5]
# zjistit jak casto se v logu objevuji chyby - pocet answers neodpovida skutecne delce,
    # chyby jsou ruzne od answers atd.
'''