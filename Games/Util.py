import pandas as pd
import re
import collections
import os.path
import numpy
import math

current_dir = os.getcwd()
parent = os.path.split(current_dir)


strilecka_session_log = pd.read_csv('%s/CSV/strilecka_session_log.csv' % (parent[0]), header = 0, sep = ';', skiprows = range(1,9046), parse_dates=['time'])
strilecka_level = pd.read_csv('%s/CSV/strilecka_level.csv' % (parent[0]), header = 0, sep = ';')
strilecka_level_word = pd.read_csv('%s/CSV/strilecka_level_word.csv' % (parent[0]), header = 0, sep = ';')

roboti_level = pd.read_csv('%s/CSV/roboti_level.csv' % (parent[0]), header = 0, sep = ';')
roboti_session_log = pd.read_csv('%s/CSV/roboti_session_log.csv' % (parent[0]), header = 0, sep = ';', parse_dates=['time'], skiprows = range(1,100))

#trva prilis dlouho, nacitame jenom pri zavolani metody
def get_roboti_shot_log():
    return pd.read_csv('%s/CSV/roboti_shot_log.csv' % (parent[0]), header = 0, sep = ';')

tetris_level = pd.read_csv('%s/CSV/tetris_level.csv' % (parent[0]), header = 0, sep = ';')
tetris_session_log = pd.read_csv('%s/CSV/tetris_session_log.csv' % (parent[0]), header = 0, sep = ';', parse_dates=['time'], skiprows = range(1,100))
tetris_vzor = pd.read_csv('%s/CSV/tetris_vzor.csv' % (parent[0]), header = 0, sep = ';')
tetris_word = pd.read_csv('%s/CSV/tetris_word.csv' % (parent[0]), header = 0, sep = ';')


class strilecka:

    id = None
    concept = None
    level = None
    words = []

    def __repr__(self):
        return '\n\n STRILECKA LEVEL\nId: ' + str(self.id)+ '\nConcept: '\
               + str(self.concept) + '\nWords: ' + str(self.words) + '\nLevel: ' + str(self.level)

#vypocita standardni odchylku pole
def standard_deviation(array_of_numbers):
    if len(array_of_numbers) < 2:
        raise ValueError("Array is too small")

    tmp = 0
    avg = numpy.mean(array_of_numbers)

    for number in array_of_numbers:
        tmp += math.pow(number - avg, 2)

    out = tmp / len(array_of_numbers)

    return math.sqrt(out)

def get_strilecka_level(id):
    s = strilecka()

    log = strilecka_level.loc[strilecka_level['id'] == id]
    s.id = id
    tmp = strilecka_level_word.loc[strilecka_level_word['level'] == id , 'word'].tolist()
    s.words = tmp
    s.level = log.level.tolist()[0]
    s.concept = log.concept.tolist()[0]

    return s

#vraci vsechny levely ve strilecce
def get_all_strilecka_level():
    all_ids = strilecka_level.id.unique()
    all_levels = []
    for id in all_ids:
        all_levels.append(get_strilecka_level(id))

    return all_levels

#print get_all_strilecka_level()