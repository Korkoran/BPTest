import pandas as pd
import re
import collections
import os.path

current_dir = os.getcwd()
parent = os.path.split(current_dir)


strilecka_session_log = pd.read_csv('%s/CSV/strilecka_session_log.csv' % (parent[0]), header = 0, sep = ';', skiprows = range(1,9046), parse_dates=['time'])
strilecka_level = pd.read_csv('%s/CSV/strilecka_level.csv' % (parent[0]), header = 0, sep = ';')
strilecka_level_word = pd.read_csv('%s/CSV/strilecka_level_word.csv' % (parent[0]), header = 0, sep = ';')

roboti_level = pd.read_csv('%s/CSV/roboti_level.csv' % (parent[0]), header = 0, sep = ';')
roboti_session_log = pd.read_csv('%s/CSV/roboti_session_log.csv' % (parent[0]), header = 0, sep = ';', parse_dates=['time'], skiprows = range(1,100))
roboti_shot_log = pd.read_csv('%s/CSV/roboti_shot_log.csv' % (parent[0]), header = 0, sep = ';')

tetris_level = pd.read_csv('%s/CSV/tetris_level.csv' % (parent[0]), header = 0, sep = ';')
tetris_session_log = pd.read_csv('%s/CSV/tetris_session_log.csv' % (parent[0]), header = 0, sep = ';', parse_dates=['time'], skiprows = range(1,100))
tetris_vzor = pd.read_csv('%s/CSV/tetris_vzor.csv' % (parent[0]), header = 0, sep = ';')
tetris_word = pd.read_csv('%s/CSV/tetris_word.csv' % (parent[0]), header = 0, sep = ';')
