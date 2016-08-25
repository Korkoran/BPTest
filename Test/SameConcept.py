import pandas as pd
import matplotlib.pyplot as plt
import Util
import Dictate

dictates = Util.getDictate()
vystup = Util.getDictateSession()
concepts = Util.CONCEPTS

numConcept = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

users = vystup.user.unique()

print len(users)

conceptNum = []
diktatyVKonceptu = []

for user in users:
    uziv = vystup.loc[vystup['user'] == user]
    #print uziv
    conceptNum = uziv.concept.unique()
    for concept in conceptNum:
        tup = (concept, len(uziv.loc[uziv['concept'] == concept, 'dictate']))
        diktatyVKonceptu.append(tup)

#print conceptNum
print len(diktatyVKonceptu)
bucket = [0]*(max(concepts)+1)
bucket2 = [0]*(max(concepts)+1)
bucket3 = [0]*(max(concepts)+1)
for (concNumber, dictatesNum) in diktatyVKonceptu:
    bucket[concNumber] += dictatesNum
    bucket2[concNumber] +=1

for i in range (len(bucket3)):
    if bucket[i] == 0:
        bucket3[i] = 0
    else:
        bucket3[i] = bucket[i] / float(bucket2[i])
print bucket3
#print len(vystup.loc[(vystup['user']==172838) & (vystup['concept']==2), 'dictate'])

