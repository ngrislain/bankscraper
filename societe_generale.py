import os
import os.path
import time
from datetime import date, timedelta, datetime
import codecs
import csv
import json
import locale
# Import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
# Import mysql connector
import MySQLdb

SG_URL = 'https://particuliers.societegenerale.fr/'
SG_CLIENT_ID = 30144911
DOWNLOAD_PATH = '/Users/nicolas/Downloads'
DB_HOST = 'grislain.fr'
DB_USER = 'bankscraper'
DB_PASSWD = 'YmFua3NjcmFwZXI='
DB_NAME = 'bankscraper'
# Set the locale of the bqnk
locale.setlocale(locale.LC_NUMERIC, 'fr_FR.UTF-8')

def get_last_download(download_path=DOWNLOAD_PATH):
    results = []
    for file in os.listdir(download_path):
        if file.endswith(".tsv"):
            results.append((os.path.join(download_path, file), time.ctime(os.path.getctime(os.path.join(download_path, file)))))
    if len(results)>0:
        return max(results, key=lambda k:k[1])[0]
    else:
        return None

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf_8')

def create_current_account_table():
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS `current_account` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `date` date DEFAULT NULL,
    `name` char(255) NOT NULL,
    `description` char(255) NOT NULL,
    `amount` decimal(12,2) NOT NULL,
    `currency` char(3) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX (`date`,`name`,`description`,`amount`,`currency`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;''')
    cur.close()
    db.commit()
    db.close()

def push_current_account_data(data):
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
    cur = db.cursor()
    cur.executemany('''INSERT IGNORE INTO `current_account` (`date`, `name`, `description`, `amount`, `currency`)
    VALUES (%s, %s, %s, %s, %s)
    ''', [(datetime.strptime(row[0], '%d/%m/%Y').date(), row[1], row[2], locale.atof(row[3]), row[4]) for row in data])
    cur.close()
    db.commit()
    db.close()

def get_transactions(sg_client_id=SG_CLIENT_ID):
    last_download = get_last_download()
    # Init a Firefox browser
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.panel.shown', True)
    profile.set_preference('browser.download.manager.showAlertOnStart', False)
    profile.set_preference('browser.download.manager.showAlertOnComplete', False)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-ecriture-txt')
    driver = webdriver.Firefox(profile)
    # Shows the login invite
    sg_url = SG_URL
    driver.get(sg_url)
    codcli = str(sg_client_id)
    driver.find_element_by_id('codcli').send_keys(codcli)
    driver.find_element_by_id('button').click()
    # Wait for the login process to complete
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/restitution/tel_telechargement.html"]'))).click()
    # Select the account to download (current account)
    select = Select(driver.find_element_by_id('compte'))
    select.select_by_index(1) # Get the first element
    # Select the format
    Select(driver.find_element_by_name('logicielFull')).select_by_value('TSV')
    # Select the date range
    datedu = (date.today()-timedelta(days=180)).strftime('%d/%m/%Y')
    driver.find_element_by_name('datedu').send_keys(datedu)
    # Get the data
    driver.find_element_by_css_selector('a[href="javascript:telecharger(this)"]').click()
    while get_last_download() == last_download:
        time.sleep(1)
    time.sleep(3)
    data = []
    with codecs.open(get_last_download(), 'r', 'latin_1') as csv_file:
        csv_reader = csv.reader(utf_8_encoder(csv_file), delimiter='\t', quotechar='"')
        csv_reader.next()
        csv_reader.next()
        names = csv_reader.next()
        for row in csv_reader:
            data.append(row)
    driver.close()
    driver.quit()
    # Push the data to mysql
    create_current_account_table()
    push_current_account_data(data)
    return names, data

names, data = get_transactions()
with open('names.json','w') as names_file:
    json.dump(names, names_file)
with open('data.json','w') as data_file:
    json.dump(data, data_file)