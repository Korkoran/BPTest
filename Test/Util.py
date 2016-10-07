import pandas as pd
import re
import collections
import os.path

current_dir = os.getcwd()
parent = os.path.split(current_dir)


dictateSession = pd.read_csv('%s/CSV/dictateSessionLog.csv' % (parent[0]), header = 0, sep = ';', parse_dates=['time'])
sessionNoNan = pd.read_csv('%s/CSV/dictateSessionLog.csv' % (parent[0]), header = 0, sep = ';', skiprows=(1,603))
dictate = pd.read_csv('%s/CSV/dictate.csv' % (parent[0]), header = 0, sep = ';')
# koncepty 5,6 nemaji zatim zaznam v session jinak
# CONCEPTS = sorted(dictate.concept.unique())
CONCEPTS = [1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
STRCONCEPTS = [str(i) for i in CONCEPTS]
#pro grafy kde se vyskytuji koncepty 5 a 6
numConcept = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

diktaty_koncepty = {
1: 'Vyjm sl B',
2: 'Vyjm sl M',
3: 'Vyjm sl P',
4: 'Shoda',
7: 'Koncovky prid',
8: 'n/nn',
9: 'me/mne',
10: 's / z',
11: 'Vyjm sl L',
12: 'Vyjm sl S',
13: 'Vyjm sl V',
14: 'Vyjm sl Z',
15: 'be/bje, me/mne',
16: 'Koncovky podst',
17: 'i/y ruzne',
18: 'Velka pis',
19: 'Sprezky',
20: 'Cizi',
21: 'Samohl',
22: 'Souhl',
23: 'Sklonovani',
24: '-ovi -ovy',
25: 'Pribeh'
}

def getDictateSession():
    return dictateSession

def getDictate():
    return dictate

class concept:

    id = None
    dictates = None
    mistakes = None
    realName = None

    def __repr__(self):
        return '\n\n CONCEPT\nId: ' + str(self.id)+ '\nReal Name: '\
               + str(self.realName) + '\nDictates: ' + str(self.dictates)

class dictat:

    id = None
    tries = None
    title = None
    concept = None
    length = None
    answers = []
    concentration = None
    mistakes = None

    def __repr__(self):
        return '\n{ DICTATE\n Id: ' + str(self.id) + '\n concept: '\
               + str(self.concept) + '\n title: ' + str(self.title) + '\n length: ' + str(self.length) +\
                "\n Mistakes: " + str(self.mistakes) +' }'

#vytvori objekt dictat nastavi atributy a vrati ho
def getDictat(dictId):
    d = dictat()

    tmp = dictate.loc[dictate['id']==dictId]
    dictText = tmp['dictate'].tolist()[0].split()
    search = dictateSession.loc[dictateSession['dictate'] == dictId]

    tmp2 = [word for word in dictText if "|" in word]

    d.id = dictId
    d.title = tmp.title.values[0]
    d.answers = tmp2
    d.tries = len(search)
    d.length = len(dictText)
    d.concept = tmp.concept.values[0]
    if len(search)!= 0:
        d.mistakes = (search.mistakes.sum() / float(len(search)))/len(d.answers)*100
    else:
        d.mistakes = 0
    d.concentration = d.length / float(len(d.answers))

    return d

#vraci pole objektu dictat
def getAllDictates():
    tmp = dictate.id.unique()

    dictates = [getDictat(d) for d in tmp]

    return dictates

#vypocita prumerny pocet chyb v konceptu
def conceptMistakes(conceptId):
    rows = len(dictateSession.loc[dictateSession['concept'] == conceptId])
    tmp = dictateSession.loc[dictateSession['concept'] == conceptId, 'mistakes'].sum()
    if rows == 0.0:
        return 0
    else:
        return tmp / float(rows)


#vraci pocet vsech chyb, ktere uzivatele udelali v diktatu s id dictId
def mistakesInDict(dictId):
    tries = len(dictateSession.loc[dictateSession['dictate']==dictId])
    if tries != 0:
        return dictateSession.loc[dictateSession['dictate']==dictId, 'mistakes'].sum()
    else:
        return 0

#vraci diktaty pro zadany koncept jako pole
def numDictates(concept):
    tmp = dictate.loc[dictate['concept'] == concept, 'id'].values.tolist()
    tmp = [int(i) for i in tmp]
    dictates = [getDictat(i) for i in tmp]
    return dictates

#vraci objekt typu concept
def getConcept(conceptNum):
    c = concept()
    c.id = conceptNum
    c.dictates = numDictates(conceptNum)
    c.realName = diktaty_koncepty[conceptNum]
    c.mistakes = conceptMistakes(conceptNum)
    return c

#vraci pole objektu typu concept
def getAllConcepts():
    all = [getConcept(concept) for concept in CONCEPTS]
    return all

def wrongWordsForConcept(conceptId):
    c = getConcept(conceptId)
    input = [getMostWrongWords(m.id) for m in c.dictates]
    return input

#vypocita skutecnou pravdepodobnost chyby v konceptu
def realConceptMistakes(concID):
    conceptDataFrame = dictateSession.loc[dictateSession['concept'] == concID]
    listOfAnswers = conceptDataFrame.answers.tolist()
    mistakes = conceptDataFrame.mistakes.sum()
    bezNan = [x for x in listOfAnswers if not isinstance(x, float)]

    lenAllAnswers = 0
    for ans in bezNan:
        lenAllAnswers += len(ans)
    if lenAllAnswers ==0:
        return 0
    return mistakes / float(lenAllAnswers) * 100


#vraci slovnik s odpovedmi a poctem spatnych odpovedi pro diktat
def getMostWrongWords(dictId):
    d = getDictat(dictId)
    answers = d.answers

    tmp = dictateSession.loc[dictateSession['dictate'] == dictId, 'answers'].values
    g = [0]*len(answers)
    newList = [x for x in tmp if str(x) != 'nan']

    for x in newList:
        #zjistit okoli chyby, najit moznou pricinu
        if len(x) > len(answers):
            print "ERROR in log, more answers than possible"
            continue
        for i in range(len(x)):
            if x[i] == "0":
                g[i] +=1

    #mistakes.append(h/float(len(newList))*100) ---- procento
    #mistakes.append(h) # ---- skutecny pocet
    mistakes = [h for h in g]

    result = collections.OrderedDict(zip(answers, mistakes))
    #result = dict(zip(answers, mistakes))
    return result


#DODELAT
def answerFormat(answer):
    if '01' in answer:
        return re.match(r"[^[]*\[([^]]*)\]", answer, re.UNICODE).groups()[0]
    if '10' in answer:
        return re.match(r"[^[]*\[([^]]*)\]", answer, re.UNICODE).groups()[0]

#vypocita procentualni zastoupeni konceptu v logu
def conceptPopularity(conceptId):
    allTries = len(dictateSession)
    conceptTries = len(dictateSession.loc[dictateSession['concept']==conceptId])
    return conceptTries/float(allTries)*100

neco = getDictat(95)

#najde pro zadane datum prvni zaznam v logu
#metoda pro DAU
#vraci id zaznamu
def getNextDateTimeFrame(time):
    return dictateSession.loc[dictateSession['time']>pd.Timestamp(time), 'id'].tolist()[0]

#predelat na nejakou normalni formu, overit jestli to sedi, zjistit cisla radku v logu
#nektere chyby jsou zasahy admina
def logError(dictId):
    session = dictateSession.loc[dictateSession['dictate']==dictId, 'answers'].tolist()
    bezNan = [x for x in session if not isinstance(x, float)]
    for n in bezNan:
        if len(n) !=len(getDictat(dictId).answers):
            print 'delka ma byt: ' + str(len(getDictat(dictId).answers))+ ' ale je: '+ str(len(n)) + ' chybna data: '+ str(n)

'''tmp = getAllDictates()
for t in tmp:
    logError(t.id)
logError(93)'''
#print getMostWrongWords(30)
#for i in range(74,80):
#    print getMostWrongWords(i).values()

''''
print getMostWrongWords(103).values()
print getDictat(103).answers[-0]
print getMostWrongWords(104).values()
#print getMostWrongWords(105).values()
print (getDictat(105).answers[0])
print getDictat(105)
print getMostWrongWords(106).values()
print getMostWrongWords(107).values()
print getMostWrongWords(108).values()
print getMostWrongWords(109).values()
print getMostWrongWords(110).values()'''
print '[' + ','.join("'" + str(x) + "'" for x in getDictat(105).answers) + ']'
print getConcept(4)
