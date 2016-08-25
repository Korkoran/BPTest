import pandas as pd
import matplotlib.pyplot as plt
import Util
from collections import Counter

dictates = pd.read_csv('CSV/dictateSessionLog.csv', header = 0, sep = ';', skiprows=602)
dictates.columns = ['id', 'user', 'concept','dictate' ,'mistakes', 'answers', 'date','gameLength' ]
print dictates.head()

dictMistakes = dictates.mistakes.tolist()
dictAnswers = dictates.answers.tolist()
#print dictAnswers

def numberOfZeros(string):
    counter = Counter(string)
    return counter['0']

tmp = []
for ans in dictAnswers:
    tmp.append(numberOfZeros(ans))

#print tmp
total = []
for i in range (len(dictMistakes)):
    if tmp[i]!=int(dictMistakes[i]):
        total.append(i + 602)

print total
#print str(total) + " z " + str(len(dictMistakes)) + " je spatne"
