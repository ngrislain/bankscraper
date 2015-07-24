import numpy as np
import scipy as sp
from scipy import stats as st
from scipy import optimize as opt
import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
import MySQLdb
from collections import Counter, defaultdict
from hiveutilities import hive
import re
from datetime import datetime, timedelta
import json
import os
from env import *

#===============================================================================
# Some tuning
#===============================================================================
mp.rcParams['axes.color_cycle'] = ['#4579DE', '#D45643', '#2D8C33', '#3F4891', '#FFE346', '#D97500', '#E884B0', '#8268B0']

#===============================================================================
# Declare constants
#===============================================================================

# Exemple
# Get alephd rules
CONNECTION = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
CURSOR = CONNECTION.cursor()

CATEGORIES = [u'alimentation',
    u'assurance',
    u'banque',
    u'énergie',
    u'épargne',
    u'garde',
    u'impôts',
    u'kiné',
    u'logement',
    u'loisirs',
    u'mobilier',
    u'ménage',
    u'salaires',
    u'santé',
    u'transport',
    u'télécom',
    u'vacances',
    u'vêtements PC',
    u'vêtements PCT']

# get client id
CURSOR.execute("""SELECT date, name, description, amount FROM current_account""")
data = CURSOR.fetchall()

for date, name, description, amount in data:
    print date, description, amount

plt.plot([date for date, name, description, amount in data], np.cumsum([amount for date, name, description, amount in data]))
plt.show()

