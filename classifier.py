# coding: utf-8 
import numpy as np
import scipy as sp
from scipy import stats as st
from scipy import optimize as opt
import pandas as pd
import matplotlib as mp
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as skl
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
import json
import os
# Some important environment variables
from env import *
# To access the database
import MySQLdb as mysql

#===============================================================================
# Some tuning
#===============================================================================
mp.rcParams['axes.color_cycle'] = ['#4579DE', '#D45643', '#2D8C33', '#3F4891', '#FFE346', '#D97500', '#E884B0', '#8268B0']

#===============================================================================
# Declare constants
#===============================================================================



class Analyser(object):
    categories = [(u'alimentation', u''),
                  (u'assurance', u''),
                  (u'banque', u''),
                  (u'énergie', u''),
                  (u'épargne', u''),
                  (u'garde', u''),
                  (u'impôts', u''),
                  (u'kiné', u''),
                  (u'logement', u''),
                  (u'loisirs', u''),
                  (u'mobilier', u''),
                  (u'ménage', u''),
                  (u'salaires', u''),
                  (u'santé', u''),
                  (u'transport', u''),
                  (u'télécom', u''),
                  (u'vacances', u''),
                  (u'vêtements PC', u''),
                  (u'vêtements PCT', u'')]
    # Create object
    def __init__(self):
        self.create_category_table()
        self.create_transaction_category_table()
        self.push_categories(self.categories)
    # Create category
    def create_category_table(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS `category` (
            `id` int(16) NOT NULL AUTO_INCREMENT,
            `label` char(255) NOT NULL,
            `description` char(255),
            PRIMARY KEY (`id`),
            UNIQUE INDEX (`label`,`description`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;''')
        cur.close()
        db.commit()
        db.close()
    # Create transaction category
    def create_transaction_category_table(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS `transaction_category` (
            `id` int(16) NOT NULL AUTO_INCREMENT,
            `transaction_id` int(16) NOT NULL,
            `category_id` int(16) NOT NULL,
            PRIMARY KEY (`id`),
            FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`id`),
            FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
            UNIQUE INDEX (`transaction_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;''')
        cur.close()
        db.commit()
        db.close()
    # Push categories to db
    def push_categories(self, categories):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.executemany('''INSERT IGNORE INTO `category` (`label`, `description`)
        VALUES (%s, %s)
        ''', categories)
        cur.close()
        db.commit()
        db.close()
    # Push transaction categories to db
    def push_transaction_categories(self, transaction_categories):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.executemany('''INSERT INTO `transaction_category` (`transaction_id`, `category_id`)
        VALUES (%s, %s)
        ''', transaction_categories)
        cur.close()
        db.commit()
        db.close()

# # get client id
# CURSOR.execute("""SELECT date, label, description, amount FROM transaction WHERE account_id='0312500050278659' ORDER BY date""")
# data = CURSOR.fetchall()
# 
# for date, name, description, amount in data:
#     print date, description, amount
# 
# plt.plot([date for date, name, description, amount in data], np.cumsum([amount for date, name, description, amount in data]))
# plt.show()

if __name__ == "__main__":
    analyser = Analyser()
