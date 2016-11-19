import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_venn import venn3, venn3_circles

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

def playing_time_mistakes():
    log = Util.dictateSession
    tooLong = 0
    for index, row in log.iterrows():
        if row['gameLength'] > 1000000:
            tooLong +=1
            continue
        if row['gameLength'] < 0:
            continue
        else:
            plt.plot(row['gameLength'], row['mistakes'], 'ro')
    plt.xlabel("cas v ms")
    plt.ylabel("pocet chyb")
    plt.show()
playing_time_mistakes()
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



# successfull_users()

def improving_users():
    pass
def returning_users():
    log = 0
    start_first = "2016-07-01"
    end_first = "2016-07-08"
    start_second = "2016-08-08"
    end_second = "2016-08-15"

    first_month_users = log.loc[(log['time'] > pd.Timestamp(start_first)) &
                                (log['time'] < pd.Timestamp(end_first)), 'user'].unique().tolist()
    second_month_users = log.loc[(log['time'] > pd.Timestamp(start_second)) &
                                 (log['time'] < pd.Timestamp(end_second)), 'user'].unique().tolist()

    out = set(first_month_users).intersection(second_month_users)
    print len(first_month_users)
    print len(second_month_users)
    print len(out)
#returning_users()
zaklad1 = 354
pole1 = [41,23,24,18,15]
zaklad2 = 529
pole2 = [55, 49, 39, 24, 22]
zaklad3 = 661
pole3 = [77, 44, 49, 28, 21]
zaklad4 = 80
pole4 =[15, 7, 8, 4, 4]

p1=[]
for p in pole1:
    p1.append(float(p)/zaklad1*100)
p2=[]
for p in pole2:
    p2.append(float(p)/zaklad2*100)
p3=[]
for p in pole3:
    p3.append(float(p)/zaklad3*100)

szaklad1 = 305
spole1=[28,17,16,4,6]
szaklad2 = 517
spole2 = [32,30,25,21,11]
szaklad3 = 720
spole3 =[67,43,24,16,11]

sp1 =[]
for p in spole1:
    sp1.append(float(p)/szaklad1*100)
sp2 =[]
for p in spole2:
    sp2.append(float(p)/szaklad2*100)
sp3 =[]
for p in spole3:
    sp3.append(float(p)/szaklad3*100)

rzaklad1 =480
rpole1=[27,32,10,18,14]
rzaklad2 = 228
rpole2 = [21,14,12,3,4]
rzaklad3 = 727
rpole3 =[86,27,28,18,10]

rp1 =[]
for p in rpole1:
    rp1.append(float(p)/rzaklad1*100)
rp2 =[]
for p in rpole2:
    rp2.append(float(p)/rzaklad2*100)
rp3 =[]
for p in rpole3:
    rp3.append(float(p)/rzaklad3*100)

print rp1
print rp2
print rp3
tydny = ["1.tyden", "2.tyden", "3.tyden", "4.tyden", "5.tyden"]

xlabels = [1,2,3,4,5]
plt.plot(xlabels, p1,'-r')
plt.plot(xlabels, p2,'-r')
plt.plot(xlabels, p3,'-r')
plt.plot(xlabels, sp1, '-b')
plt.plot(xlabels, sp2, '-b')
plt.plot(xlabels, sp3, '-b')
plt.plot(xlabels, rp1, '-g')
plt.plot(xlabels, rp2, '-g')
plt.plot(xlabels, rp3, '-g')
red_patch = mpatches.Patch(color='red', label='Diktaty')
green_patch = mpatches.Patch(color='green', label='Roboti')
blue_patch = mpatches.Patch(color='blue', label='Strilecka')
plt.legend(handles=[red_patch, green_patch, blue_patch])
plt.ylabel("% uzivatelu")
plt.xticks(xlabels, tydny)
plt.grid(True)
plt.xticks()
plt.xlim([0.5, 5.5])
plt.show()
