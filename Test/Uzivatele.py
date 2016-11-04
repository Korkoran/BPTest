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
# concepts_per_user()

def successfull_users():
    vystup = Util.getDictateSession()

    users = vystup.user.unique()
    good_users = []
    bad_users = []
    for user in users:
        tmp = vystup.loc[vystup['user'] == user]
        if len(tmp) > 10:
            succ = 0
            dictates = tmp.dictate.unique()
            for dictat in dictates:
                n = tmp.loc[tmp['dictate'] == dictat, 'answers'].tolist()[0]
                if type(n) == str:
                    c = n.count('0')
                    if dictat == 0 or dictat == -1:
                        continue
                    if c > Util.getDictat(dictat).mistakes:
                        succ -= 1
                    else:
                        succ += 1
            if succ > 0:
                good_users.append(user)
            else:
                bad_users.append(user)

    print len(good_users)
    print len(bad_users)


successfull_users()

def improving_users():
    pass
