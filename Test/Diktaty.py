import matplotlib.pyplot as plt
import pandas as pd

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
print "++++++++++" + str(pokusy) + "++++++++"
for dict in dictText:
    delky.append(len(dict.split()))
    splited = dict.split()
    pocet = 0
    #nepocita slova spravne napr. [po tom/potom|01]
    for word in splited:
        if "|" in word:
            pocet +=1
    odpovedi.append(pocet)

#print len(delky)
#print len(chyby)

print odpovedi
print len(odpovedi)


pomer = []
for i in range(len(delky)):
    pomer.append(chyby[i]/delky[i])
    pomerChyb.append(chyby[i]/float(odpovedi[i])*100)
print "<<<<<<<<" + str(odpovedi) + ">>>>>>"
print "<<<<<<<<" + str(chyby) + ">>>>>>"
print "<<<<<<<<" + str(pomerChyb) + ">>>>>>"
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

plt.show()
plt.title('')
plt.xlabel('Delka diktatu')
plt.ylabel('procento chyb')
plt.plot(delky, pomerChyb, 'bo')
plt.show()
