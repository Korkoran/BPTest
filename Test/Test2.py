import pandas as pd
import matplotlib.pyplot as plt

import Util

vystup = Util.getDictateSession()
dictates = Util.getDictate()
dictId = dictates.id.unique()
print dictId
tries = []

concepts = [1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
numConcept = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

for concept in concepts:
    tries.append(len(vystup.loc[vystup['concept'] == concept]))

print tries
soucet = sum(tries) / len(concepts)
concepts2 = [str(i) for i in concepts]

plt.bar(numConcept,tries, align='center', color='red')
#plt.barh(tries,numConcept, align='center', color='red')
plt.xticks(numConcept, concepts2)
plt.grid(True)
plt.title('Pocet vyplneni uzivateli')
plt.xlabel('Koncept')
plt.ylabel('Vyplneni')

plt.show()

