import pandas as pd
import matplotlib.pyplot as plt

import Util

def concepts_per_user():
    dictates = Util.getDictate()
    vystup = Util.getDictateSession()

    users = vystup.user.unique()

    conceptNum = []

    for user in users:
        concepts = []
        concepts =  vystup.loc[vystup['user'] == user, 'concept']
        conceptNum.append(concepts.unique().size)


    labels = '1', '2', '3', '4', '5', '6+'

    explode = (0.1,0.1,0.1,0.2,0.1,0.2)

    vysl = [0]*(max(conceptNum)+1)

    for conc in conceptNum:
        vysl[conc] += 1

    print vysl[1:]

    zbytek = sum(vysl[6:])

    konec = vysl[1:6]
    pole = range(1,9)

    konec.append(zbytek)

    print "Pocet uzivatelu s vyssim poctem vyzkousenych konceptu: " + str(len(users) - zbytek)
    plt.pie(konec, labels=labels, startangle=0, explode=explode, autopct='%1.1f%%')

    plt.title('Kolik konceptu uzivatel vyzkousi')
    plt.show()
concepts_per_user()
