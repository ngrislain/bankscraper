import keyring
# Some important environment variables
from env import *
# To access accounts
from weboob.core import Weboob
from weboob.capabilities.bank import CapBank
# To access the database
import MySQLdb as mysql

class scraper(object):
    def __init__(self):
        self.create_account_table()
        self.create_transaction_table()
    
    def scrape_accounts(self, holder):
        web = Weboob()
        web.load_backends(CapBank)
        backend = web.get_backend('societegenerale')
        backend.config['login'].set(keyring.get_password('fr.grislain.societegenerale.login', holder))
        backend.config['password'].set(keyring.get_password('fr.grislain.societegenerale.password', holder))
        # get accounts
        for account in backend.iter_accounts():
            self.insert_account(account)
            self.scrape_transactions(backend, account)
    
    def scrape_transactions(self, backend, account):
        for transaction in backend.iter_history(account):
            print transaction
    
    def create_account_table(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS `account` (
        `id` int(32) NOT NULL,
        `label` char(255) NOT NULL,
        `currency` char(3) NOT NULL,
        PRIMARY KEY (`id`),
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
        cur.close()
        db.commit()
        db.close()
    
    def create_transaction_table(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS `transaction` (
        `id` int(16) NOT NULL AUTO_INCREMENT,
        `date` date DEFAULT NULL,
        `label` char(255) NOT NULL,
        `description` char(255) NOT NULL,
        `amount` decimal(12,2) NOT NULL,
        `account_id` int(32) NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`account_id`) REFERENCES account (`id`),
        UNIQUE INDEX (`date`,`label`,`description`,`amount`,`account_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;''')
        cur.close()
        db.commit()
        db.close()

s = scraper()
s.scrape_accounts('nicolas')


# # get history
# for transaction in backend.iter_history(account):
#     print transaction
# 
# transactions = list(backend.iter_history(account))
# 
# transactions[0].date
# transactions[0].category
# transactions[0].label
# transactions[0].raw
# transactions[0].amount
# account.currency

#`name`,`description`,`amount`,`currency`


 
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