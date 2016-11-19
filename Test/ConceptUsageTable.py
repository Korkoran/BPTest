import numpy as np
import matplotlib.pyplot as plt
import ConceptUsage as CU
import Util

concepts= CU.conceptUsage()

concepts.sort(key=lambda  x: x.popularity, reverse=True)

#concepts = concepts[0:11]

neco = []
arrays = [[] for i in range(len(concepts))]
ids = [conc.id for conc in concepts]
for i in range(len(arrays)):
    arrays[i].append(Util.diktaty_koncepty[concepts[i].id])
    arrays[i].append(str("%.1f " % concepts[i].avarageUse + '%'))
    arrays[i].append(str("%.1f " % concepts[i].completePr + '%'))
    arrays[i].append(str("%.1f " % concepts[i].popularity))

col_labels = ['Koncept','Prumerne vyuziti', 'Vyuzity vsechny', 'Popularita konceptu']
row_labels = ids
table_vals = arrays
table = plt.table(cellText = table_vals,
                  rowLabels = row_labels,
                  colLabels = col_labels,
                  loc = 'center')
plt.axis('off')
table.scale(1,1)
plt.show()

