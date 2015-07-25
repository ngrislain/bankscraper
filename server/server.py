from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from MySQLdb import connect
from env import *

class MainHandler(RequestHandler):
    connection = connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME)
    cursor = connection.cursor()
    def get(self):
        self.cursor.execute("""SELECT date, name, description, amount FROM current_account ORDER BY date""")
        transactions = self.cursor.fetchall()
        self.render("index.html", transactions=transactions)

if __name__ == "__main__":
    application = Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    IOLoop.current().start()