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

concepts = Util.getAllConcepts()

out_conc_numbers = []
out_dict_mistakes = []
for concept in concepts:
    for dictate in concept.dictates:
        out_conc_numbers.append(concept.id)
        out_dict_mistakes.append(dictate.mistakes)

plt.plot(out_conc_numbers, out_dict_mistakes, 'ro')
plt.grid(True)
plt.xticks(range(0,26), range(0,26))
plt.show()

