# Some important environment variables
from env import *
# To access the database
import MySQLdb as mysql

class Database(object):
    # Enter connection
    def __enter__(self):
        self.db = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
        self.cur = self.db.cursor()
        return self
    # Exit connection
    def __exit__(self, type, value, traceback):
        self.cur.close()
        self.db.commit()
        self.db.close()
    # Get accounts
    def get_accounts(self):
        self.cur.execute('''SELECT * FROM `account`''')
        return self.cur.fetchall()
    # Get categories
    def get_categories(self):
        self.cur.execute('''SELECT * FROM `category`''')
        return self.cur.fetchall()
    # Get transactions
    def get_transactions(self, account):
        self.cur.execute('''SELECT `id`, `date`, `label`, `description`, `amount` FROM `transaction` WHERE `account_id`=%s ORDER BY `date`''', (account[0],))
        return self.cur.fetchall()