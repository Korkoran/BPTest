import pandas as pd

dictateSession = pd.read_csv('CSV/dictateSessionLog.csv', header = 0, sep = ';')
dictate = pd.read_csv('CSV/dictate.csv', header = 0, sep = ';')
# koncepty 5,6 nemaji zatim zaznam v session jinak
# CONCEPTS = sorted(dictate.concept.unique())
CONCEPTS = [1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

diktaty_koncepty = {
1: 'Vyjm sl B',
2: 'Vyjm sl M',
3: 'Vyjm sl P',
4: 'Shoda',
7: 'Koncovky prid',
8: 'n/nn',
9: 'me mne',
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

    def __repr__(self):
        return '\n{ DICTATE\n Id: ' + str(self.id) + '\n concept: '\
               + str(self.concept) + '\n title: ' + str(self.title) + '\n length: ' + str(self.length)+' }'

#vytvori objekt dictat nastavi atributy a vrati ho
def getDictat(dictId):
    d = dictat()
    d.id = dictId

    tmp = dictate.loc[dictate['id']==dictId]

    d.title = tmp.title.values[0]
    d.concept = tmp.concept.values[0]
    dictText = tmp['dictate'].tolist()[0].split()
    d.length = len(dictText)
    d.tries = len(dictateSession[dictateSession['dictate']==dictId])

    for word in dictText:
        if "|" in word:
            d.answers.append(word)

    d.concentration = d.length / float(len(d.answers))

    return d

#vraci pole objektu dictat
def getAllDictates():
    tmp = dictate.id.unique()
    dictates = []
    for d in tmp:
        dictates.append(getDictat(d))

    return dictates

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
    dictates = []
    for i in tmp:
        dictates.append(getDictat(i))
    return dictates

#vraci objekt typu concept
def getConcept(conceptNum):
    c = concept()
    c.id = conceptNum
    c.dictates = numDictates(conceptNum)
    c.realName = diktaty_koncepty[conceptNum]
    return c

#vraci pole objektu typu concept
def getAllConcepts():
    all = []
    for concept in CONCEPTS:
        all.append(getConcept(concept))
    return all

print getDictat(4).tries
print 'ahoj\xc3\xa9'.decode('utf-8')
print 'dacan\xc3\xa9'

print mistakesInDict(4)