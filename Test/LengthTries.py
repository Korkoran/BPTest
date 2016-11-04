import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import Util
import numpy as np


concept = Util.getConcept(20)

out = []
dictId = []

dictates = concept.dictates
for dictate in dictates:
    dictId.append(dictate.id)
    mistakes = Util.mistakesInDict(dictate.id)
    out.append(float(mistakes)/dictate.tries)
    #print str(dictate.length) + ' ' + str(dictate.tries)

#newlist = sorted(Util.getAllDictates(), key = lambda x: x.length, reverse=True)

#print newlist


veryPopular= (Util.getConcept(1).dictates + Util.getConcept(4).dictates)
mediumPopular = (Util.getConcept(2).dictates + Util.getConcept(7).dictates+ Util.getConcept(10).dictates+ Util.getConcept(16).dictates+
                 Util.getConcept(17).dictates+ Util.getConcept(18).dictates+ Util.getConcept(24).dictates+ Util.getConcept(25).dictates)
lowPopularity = (Util.getConcept(3).dictates+ Util.getConcept(8).dictates+ Util.getConcept(9).dictates+ Util.getConcept(11).dictates+ Util.getConcept(12).dictates+
                 Util.getConcept(13).dictates+ Util.getConcept(14).dictates+ Util.getConcept(15).dictates+ Util.getConcept(19).dictates+ Util.getConcept(20).dictates+
                 Util.getConcept(21).dictates+ Util.getConcept(22).dictates+ Util.getConcept(23).dictates)

print len(veryPopular)
print len(mediumPopular)
print len(lowPopularity)
'''
tmp1 = sorted(veryPopular, key=lambda x: len(x.answers), reverse=True)
tmp2 = sorted(mediumPopular, key=lambda y: len(y.answers), reverse=True)
tmp3 = sorted(lowPopularity, key=lambda z: len(z.answers), reverse=True)
'''
tmp1 = sorted(veryPopular, key=lambda x: x.length, reverse=True)
tmp2 = sorted(mediumPopular, key=lambda y: y.length, reverse=True)
tmp3 = sorted(lowPopularity, key=lambda z: z.length, reverse=True)


length1 = []
tries1 = []

length2 = []
tries2 = []

length3 = []
tries3 = []

for t in tmp1:
    length1.append(t.length)
    tries1.append(t.tries)

for t in tmp2:
    length2.append(t.length)
    tries2.append(t.tries)

for t in tmp3:
    length3.append(t.length)
    tries3.append(t.tries)
'''
for t in tmp1:
    length1.append(len(t.answers))
    tries1.append(t.tries)

for t in tmp2:
    length2.append(len(t.answers))
    tries2.append(t.tries)

for t in tmp3:
    length3.append(len(t.answers))
    tries3.append(t.tries)
'''
fit1 = np.polyfit(length1,tries1,2)
fit_fn1 = np.poly1d(fit1)

fit2 = np.polyfit(length2,tries2,2)
fit_fn2 = np.poly1d(fit2)

fit3 = np.polyfit(length3,tries3,2)
fit_fn3 = np.poly1d(fit3)

print tries1
print length1
print length2

plt.plot(length1, tries1, 'ro', length1, fit_fn1(length1), '-r')
plt.plot(length2, tries2, 'bo', length2, fit_fn2(length2), '-b')
plt.plot(length3, tries3, 'go', length3, fit_fn3(length3), '-g')
'''
plt.plot(length1, tries1, 'ro')
plt.plot(length2, tries2, 'bo')
plt.plot(length3, tries3, 'go')
'''
plt.title("Graf 2")
plt.xlabel("Delka diktatu")
plt.ylabel("Pocet vyplneni")

red_dot = mpatches.Patch(color='red', label = 'Velmi popularni koncept')
blue_dot = mpatches.Patch(color='blue', label = 'Prumerne popularni koncept')
green_dot = mpatches.Patch(color='green', label = 'Malo popularni koncept')

plt.legend(handles = [red_dot, blue_dot, green_dot])
plt.axis([40,180,0,500])
plt.show()