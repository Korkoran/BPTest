import numpy as np
import matplotlib.pyplot as plt
import ConceptUsage as CU

concepts= CU.conceptUsage()

concepts.sort(key=lambda  x: x.popularity, reverse=True)

neco = []
arrays = [[] for i in range(len(concepts))]
ids = [conc.id for conc in concepts]
print arrays
print ids
for i in range(len(arrays)):
    arrays[i].append(concepts[i].id)
    arrays[i].append(str("%.1f " % concepts[i].avarageUse + '%'))
    arrays[i].append(str("%.1f " % concepts[i].completePr + '%'))
    arrays[i].append(str("%.1f " % concepts[i].popularity))
print arrays
print("%.1f " % 30.006906077348066) + '%'
col_labels = ['Koncept','prumerne', 'vsechny', 'popularita']
row_labels = ids
table_vals = arrays
table = plt.table(cellText = table_vals,
                  rowLabels = row_labels,
                  colLabels = col_labels,
                  loc = 'center')
plt.axis('off')
table.scale(1,1)
plt.show()

