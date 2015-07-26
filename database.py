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
    def get_transactions(self, account_id=None, category_id=None):
        where_conditions = []
        ids = []
        if account_id:
            if account_id=='null':
                where_conditions.append('`transaction`.`account_id` IS NULL')
            else:
                where_conditions.append('`transaction`.`account_id`=%s')
                ids.append(account_id)
        if category_id:
            if category_id=='null':
                where_conditions.append('`transaction_category`.`category_id` IS NULL')
            else:
                where_conditions.append('`transaction_category`.`category_id`=%s')
                ids.append(int(category_id))
        self.cur.execute('''SELECT `transaction`.`id`, `transaction`.`date`, `transaction`.`label`, `transaction`.`description`, `transaction`.`amount`, `transaction`.`account_id`, `category`.`label` FROM
                `transaction`
                LEFT JOIN `transaction_category` ON `transaction`.`id`=`transaction_category`.`transaction_id`
                LEFT JOIN `category` ON `transaction_category`.`category_id`=`category`.`id`'''
        +(' WHERE '+' AND '.join(where_conditions) if len(ids)>0 else '')
        +''' ORDER BY `transaction`.`date`''', ids)
        return self.cur.fetchall()
    # Push transaction categories
    def push_transaction_categories(self, transaction_categories):
        self.cur.executemany('''INSERT INTO `transaction_category` (`transaction_id`, `category_id`)
        VALUES (%s, %s)
        ''', transaction_categories)
        return