import pandas as pd
import matplotlib.pyplot as plt
import Util
import collections

dictates = Util.getDictate()
vystup = Util.getDictateSession()
dictId = dictates.id.unique()
print dictId
mistakes = []
dict = {}


for dictate in dictId:
    d = Util.dictat()
    pokusy = len(vystup.loc[vystup['dictate'] == dictate])
    d.tries = pokusy
    d.id = dictate
    d.concept = vystup.loc[vystup['dictate']]
    if pokusy != 0:
        mistakes.append(vystup.loc[vystup['dictate'] == dictate, 'mistakes'].sum() / float(pokusy))
    else:
        mistakes.append(0)

def getMistakes():
    return mistakes




plt.bar(dictId, mistakes)
plt.show()