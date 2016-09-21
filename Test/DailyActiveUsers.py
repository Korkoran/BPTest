import pandas as pd
import Util

log= Util.dictateSession

times = log.time.tolist()

#vrati pocet unikatnich pristupu za den
def DAU(date):
    out = []
    for time in times:
        if str(time).split()[0] ==date:
            tmp=  log.loc[log['time']==time, 'user'].tolist()
            for t in tmp:
                out.append(t)

    myset = set(out)
    return len(myset)
DAU("2016-09-05")

#vypocita v jake hodiny byly ulozeny zaznamy mezi startDate a endDate
#startDate a endDate se musi nachazet v logu
def accessHours(startDate, endDate):
    clock = [0 for x in range(0,24)]
    userClock = [[] for x in range(0,24)]

    start =Util.getNextDateTimeFrame(startDate)
    end = Util.getNextDateTimeFrame(endDate)

    #start= log.loc[log['time']==startDate, 'id'].tolist()[0]
    #end = log.loc[log['time']==endDate, 'id'].tolist()[0]

    tmp = start

    newLog = log.loc[(log['id'] >= start) & (log['id']<= end) ]

    users = []
    while tmp < end:
        #celkovy pocet logu ne pocet unikatnich uzivatelu
        #upravit na jeden .loc
        date= str(newLog.loc[newLog['id'] == tmp, 'time'].tolist()[0])

        #pruser, pocita navic uzivatele kteri se prihlasili v ruznych hodinach
        user = newLog.loc[newLog['id']== tmp, 'user'].tolist()[0]

        time = date.split()[1]
        hour = time.split(':')[0]
        clock[int(hour)] +=1
        userClock[int(hour)].append(user)
        tmp +=1

    #prevod na mnozinu k odstraneni duplikatu
    for i in range(len(userClock)):
        myset = set(userClock[i])
        myList = list(myset)

        #odstraneni duplikatu pri prechodu pres celou hodinu
        userClock[i] = len(myset)



    print userClock
    print sum(userClock)

accessHours("2016-09-13", "2016-09-14")