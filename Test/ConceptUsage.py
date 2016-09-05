import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import Util
import copy

numConcept = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

'''
zjisti jake procento diktatu uzivatel vyzkousi v jakem konceptu - jake koncepty je treba rozsirit
zjisti kolik procent uzivatelu vyzkouselo vsechny diktaty v konceptu
'''
def conceptUsage():
    session = Util.dictateSession
    concepts = Util.getAllConcepts()
    arrays = [[] for i in range(max(concept.id for concept in concepts)+1)]
    complete = [0]* 26

    for concept in concepts:
        tmp = session.loc[session['concept'] == concept.id]
        uzivatele = tmp.user.unique()

        number_of_dictates = len(concept.dictates)

        for user in uzivatele:
            divided = len(tmp.loc[tmp['user']== user, 'dictate'].unique()) / float(number_of_dictates)
            arrays[concept.id].append(divided)


        if concept.id == 4:
            print type(uzivatele[0])
            print number_of_dictates

    print arrays[12]
    for i in range(len(arrays)):
        length = len(arrays[i])
        if i == 3:
            print arrays[3]
        for j in arrays[i]:
            if j == 1:
               complete[i] +=1
        if length!=0:
            arrays[i] = (sum(arrays[i]) / float(length)) *100
            complete[i] = (complete[i] / float(length)) *100
        else:
            arrays[i] = 0
        #complete[i] = complete[i] / length


    print complete
    print arrays[12]
    result = dict(zip(range(0,26), arrays))
    print result
    print len(arrays)

    plt.bar(numConcept, arrays, align='center')
    plt.xticks(range(0,26), range(0,26))
    plt.bar(numConcept, complete, color = 'g', align='center')
    plt.title('')

    blue = mpatches.Patch(color= 'blue', label = 'Procento vyzkousenych diktatu')
    green = mpatches.Patch(color= 'green', label = 'Vsechny diktaty')

    plt.legend(handles = [blue, green])
    plt.axis([0, 26, 0, 80])
    columns = ('dikataty', 'uzivatele')
    cellText = [arrays, complete]
    plt.table(cellText = cellText, rowLabels = concepts, colLabels = columns, loc= 'bottom')
    plt.show()


conceptUsage()