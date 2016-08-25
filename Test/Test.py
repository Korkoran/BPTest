import pandas as pd
import datetime
import pandas.io.data as web
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import Util


vystup = Util.getDictateSession()
averages = []
tries = []
print vystup.head()

#Zkusit stahnout novou verzi dictatesession a pridat 5,6
concepts = Util.CONCEPTS
for concept in concepts:
    time = 0
    if float(len(vystup.loc[vystup['concept'] == concept])) == 0.0:

        averages.append(0)
    else:
        print "!!!!!!!!" + str(float(len(vystup.loc[vystup['concept'] == concept])))
        averages.append(vystup.loc[vystup['concept'] == concept, 'mistakes'].sum() / float(len(vystup.loc[vystup['concept'] == concept])))

    tries.append(len(vystup.loc[vystup['concept'] == concept]))
    print ("Concept number: "+str(concept) +"  Avarage mistakes: "
           + str(vystup.loc[vystup['concept'] == concept, 'mistakes'].sum() / len(vystup.loc[vystup['concept'] == concept]))
           + " Number of tries: " + str(len(vystup.loc[vystup['concept'] == concept]))
           + " Avarage time spent: " + str(vystup.loc[vystup['concept'] == concept, 'gameLength'].sum() / len(vystup.loc[vystup['concept'] == concept])))

print vystup.loc[vystup['user'] == 172838, 'mistakes'].sum()

#vystup['tries'] = tries

print vystup

absoluteAverageTime = (vystup['gameLength']).sum() / float(len(vystup))
absoluteMistakes = (vystup['mistakes']).sum() / float(len(vystup))

print "Absolute average time is: " + str(absoluteAverageTime)
print "Absolute average mistakes is: " + str(absoluteMistakes)
print len(vystup)
#neco = vystup.loc[vystup['concept'] == 1, 'mistakes'].sum() / float(len(vystup.loc[vystup['concept'] == 1]))
print vystup.loc[vystup['concept'] == 1, 'mistakes'].sum() / float(len(vystup.loc[vystup['concept'] == 1]))
print (vystup['mistakes']).sum()
print averages
def getAverages():
    return averages

concepts2 = [str(i) for i in concepts]
vystu = averages
numConcept = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
hist = ['1','1','1','1','2','2','3','3','3','4','4','7','7','7','9','9','10','10','10','11','11','12','12','12','13','13','13','14','14','15','15','16','16','16','17','17','17','18','18','18','18','18']
print tries
#plt.plot(concepts, neco, 'ro')
#plt.xticks(concepts)
#plt.margins(0.5)
plt.xlabel('concept number')
plt.ylabel('average mistakes')
#plt.hist(hist, bins = concepts, facecolor = 'green')
#plt.xticks(concepts)
plt.grid(True)

plt.bar(numConcept,
        vystu,
        align='center',
        #yerr = [0.2,1,1,1,1,0,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22],
        color = 'g')
#plt.bar(numConcept, tries, align='center', color='red')
plt.xticks(numConcept, concepts2)
plt.axis([0,24,0,7])
plt.axhline(y=absoluteMistakes, color = 'green')
plt.text(3.5,3.6, "overall average")
plt.title('Average mistakes by concept')
plt.show()