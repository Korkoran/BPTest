import pandas as pd
import matplotlib.pyplot as plt
import Util
from collections import Counter


#print str(total) + " z " + str(len(dictMistakes)) + " je spatne"
log = Util.dictateSession
print len(log.loc[log['gameLength'] > 600000])