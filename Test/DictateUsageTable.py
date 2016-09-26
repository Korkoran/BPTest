import matplotlib.pyplot as plt
import Util
import pandas as pd

concepts = Util.CONCEPTS
dictates = Util.dictateSession

diktaty = Util.getAllDictates()

diktaty.sort(key=lambda x: x.mistakes, reverse=True)

out = []
diff = []


for d in diktaty:
    diktat = []
    #print d.mistakes
    diktat.append(str(d.id))
    diktat.append(str(d.concept))
    diktat.append(str("%.1f " % d.mistakes + '%'))
    diktat.append(str("%.1f " % Util.realConceptMistakes(d.concept) + '%'))
    if d.mistakes > Util.realConceptMistakes(d.concept) +4:
        diff.append(diktat)
    if d.mistakes + 4 < Util.realConceptMistakes(d.concept):
        diff.append(diktat)

    #diktat.append(conceptDataFrame.mistakes.sum()/conceptDataFrame.)
    out.append(diktat)
    #arrays[i].append(str("%.1f " % concepts[i].avarageUse + '%'))


print out
print diff
col_Labels = ['Diktat Id', 'Koncept Id', 'Sance na chybu', 'Prumer v konceptu']

table = plt.table(cellText = out[0:20],
                  colLabels = col_Labels,
                  loc = 'center')
plt.show()