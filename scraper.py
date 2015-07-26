import schedule
import logging
import keyring
# Some important environment variables
from env import *
# To access accounts
from weboob.core import Weboob
from weboob.capabilities.bank import CapBank
# To access the database
import MySQLdb as mysql

class Scraper(object):
    def __init__(self):
        self.create_account_table()
        self.create_transaction_table()
    # Get last transactions from holder account
    def scrape_accounts(self, holder):
        web = Weboob()
        web.load_backends(CapBank)
        backend = web.get_backend('societegenerale')
        backend.config['login'].set(keyring.get_password('fr.grislain.societegenerale.login', holder))
        backend.config['password'].set(keyring.get_password('fr.grislain.societegenerale.password', holder))
        # get accounts
        for account in backend.iter_accounts():
            self.push_account(account)
            self.scrape_transactions(backend, account)
    # Get the transactions and push them
    def scrape_transactions(self, backend, account):
        self.push_transactions(backend.iter_history(account), account)
    # Create account
    def create_account_table(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS `account` (
        `id` char(32) NOT NULL,
        `label` char(255) NOT NULL,
        `currency` char(3) NOT NULL,
        PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;''')
        cur.close()
        db.commit()
        db.close()
    # Create transaction
    def create_transaction_table(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS `transaction` (
        `id` int(16) NOT NULL AUTO_INCREMENT,
        `date` date DEFAULT NULL,
        `label` char(255) NOT NULL,
        `description` char(255) NOT NULL,
        `amount` decimal(12,2) NOT NULL,
        `account_id` char(32) NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
        UNIQUE INDEX (`date`,`label`,`description`,`amount`,`account_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;''')
        cur.close()
        db.commit()
        db.close()
    # Push account to db
    def push_account(self, account):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''INSERT IGNORE INTO `account` (`id`, `label`, `currency`)
        VALUES (%s, %s, %s)
        ''', (account.id, account.label, account.currency))
        cur.close()
        db.commit()
        db.close()
    # Push transaction to db
    def push_transactions(self, transactions, account):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.executemany('''INSERT IGNORE INTO `transaction` (`date`, `label`, `description`, `amount`, `account_id`)
        VALUES (%s, %s, %s, %s, %s)
        ''', [(transaction.date, transaction.category, transaction.raw, transaction.amount, account.id) for transaction in transactions])
        cur.close()
        db.commit()
        db.close()
    # Push legacy data
    def push_old_transactions(self):
        db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        cur = db.cursor()
        cur.execute('''SELECT `date`, `name`, `description`, `amount` FROM `current_account`''')
        transactions = cur.fetchall()
        cur.executemany('''INSERT IGNORE INTO `transaction` (`date`, `label`, `description`, `amount`, `account_id`)
        VALUES (%s, %s, %s, %s, '0312500050278659')
        ''', transactions)
        cur.close()
        db.commit()
        db.close()

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Starting scraper')
    # Define the update function
    def update():
        logging.info('Scraping')
        scraper = Scraper()
        logging.info('Get transactions for nicolas')
        scraper.scrape_accounts('nicolas')
        logging.info('Get transactions for celine')
        scraper.scrape_accounts('celine')
    # Schedule updates
    while True:
        schedule.every().hour.do(update)
        schedule.run_pending()