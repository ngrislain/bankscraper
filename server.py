import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, StaticFileHandler
from database import Database

class MainHandler(RequestHandler):
    def get(self):
        with Database() as db:
            accounts = db.get_accounts()
            account = next(account for account in accounts if account[1]=='Compte Bancaire')
#             self.render("server/index.html", transactions=db.get_transactions(account))
            self.render("server/index.html", transactions=db.get_transactions(account))

class APIHandler(RequestHandler):
    def get(self, request):
        if request=='account':
            with Database() as db:
                self.write(json.dumps([(id, label, currency) for id, label, currency in db.get_accounts()]))
        elif request=='category':
            with Database() as db:
                self.write(json.dumps([(id, label, description) for id, label, description in db.get_categories()]))
        elif request=='transaction':
            with Database() as db:
                accounts = db.get_accounts()
                if len(self.get_arguments('id'))>0:
                    account = next(account for account in accounts if account[0]==self.get_arguments('id')[0])
                elif len(self.get_arguments('label'))>0:
                    account = next(account for account in accounts if account[1]==self.get_arguments('label')[0])
                else:
                    account = next(account for account in accounts if account[1]=='Compte Bancaire')
                self.write(json.dumps([(date.isoformat(), label, description, float(amount)) for date, label, description, amount in db.get_transactions(account)]))
        


if __name__ == "__main__":
    handlers = [
                (r'/static/(.*)', StaticFileHandler, {'path': 'server/'}),
                (r'/api/(.*)', APIHandler),
                (r'/', MainHandler)
                ]
    application = Application(handlers)
    application.listen(8888)
    IOLoop.current().start()