from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from database import Database

class MainHandler(RequestHandler):
    def get(self):
        with Database() as db:
            accounts = db.get_accounts()
            account = next(account for account in accounts if account[1]=='Compte Bancaire')
            for t in db.get_transactions(account):
                print t
            self.render("server/index.html", transactions=db.get_transactions(account))

if __name__ == "__main__":
    application = Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    IOLoop.current().start()