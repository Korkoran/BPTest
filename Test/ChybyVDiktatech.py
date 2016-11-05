import pandas as pd
import matplotlib.pyplot as plt
import Util
import collections

dictates = Util.getDictate()
vystup = Util.getDictateSession()
dictId = dictates.id.unique()
mistakes = []
dict = {}



data = [(1, 1), (2, 3),
        (2, 2), (4, 5),
        (5, 5), (6, 7)]
print data
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




# plt.bar(dictId, mistakes)
# plt.show()

concepts = Util.getAllConcepts()

out_conc_numbers = []
out_dict_mistakes = []
out = []
conc = []
for concept in concepts:
    tmp = []
    for dictate in concept.dictates:
        out_conc_numbers.append(concept.id)
        out_dict_mistakes.append(dictate.mistakes)
        tmp.append(dictate.mistakes)

    out.append((max(tmp), min(tmp)))
    conc.append((concept.id, concept.id))
data = []
for i in range(len(out)):
    data.append(conc[i])
    data.append(out[i])
print data

lines = plt.plot(*data)
plt.setp(lines, linewidth = 3)
plt.plot(out_conc_numbers, out_dict_mistakes, 'ro')
plt.xlabel("Koncepty")
plt.ylabel("Chyby")
plt.grid(True)
plt.xticks(range(0,26), range(0,26))
plt.xlim([0,26])
plt.show()

plt.plot(out_conc_numbers, out_dict_mistakes, 'ro')
plt.xlabel("Koncepty")
plt.ylabel("Diktaty")
plt.grid(True)
plt.xticks(range(0,26), range(0,26))
plt.show()

