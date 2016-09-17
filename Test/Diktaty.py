import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import ChybyVDiktatech as ch
import Util

dictates = Util.getDictate()
vystup = Util.getDictateSession()

dict = dictates.concept.unique()
print "!!!!!!!!!!!!!!!" + str(dict)
dictId = dictates.id.tolist()
dictText = dictates.dictate.tolist()

delky = []
chyby = ch.getMistakes()
odpovedi = []
pomerChyb = []
pokusy = []

#pridat modifikator podle konceptu
for d in dictId:
    pokusy.append(len(vystup.loc[vystup['dictate'] == d]))
for dict in dictText:
    delky.append(len(dict.split()))
    splited = dict.split()
    pocet = 0
    #nepocita slova spravne napr. [po tom/potom|01]
    for word in splited:
        if "|" in word:
            pocet +=1
    odpovedi.append(pocet)

print odpovedi
print len(odpovedi)


pomer = []
for i in range(len(delky)):
    pomer.append(chyby[i]/delky[i])
    pomerChyb.append(chyby[i]/float(odpovedi[i])*100)

for i in range(len(dictId)):
    print "diktat cislo: " + str(dictId[i])+ "ma delku " + str(delky[i]) + " ma pomer slov/odpovedi "+\
          str(float(odpovedi[i])/delky[i]*100)+ " prumerny pocet chyb " + str(chyby[i]) + " pomer chyb vyhledem k delce " + str(pomer[i]*100) + " / " + str(pomerChyb[i])
print len(pomerChyb)
plt.title('')
plt.ylabel('Pocet pokusu')
plt.xlabel('Delka diktatu')
plt.plot(delky, pokusy, 'ro')

def getPomer():
    return pomerChyb

fit = np.polyfit(delky,pomerChyb,1)
fit_fn = np.poly1d(fit)

plt.show()
plt.title('')
plt.xlabel('Delka diktatu')
plt.ylabel('procento chyb')
plt.plot(delky, pomerChyb, 'bo', delky, fit_fn(delky), '--k')
plt.show()
