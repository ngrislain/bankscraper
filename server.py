import json
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, StaticFileHandler
from database import Database

class HomeHandler(RequestHandler):
    def get(self):
        with Database() as db:
            self.render("server/index.html")

class CategoriesHandler(RequestHandler):
    def get(self):
        with Database() as db:
            self.render("server/categories.html", transactions=db.get_transactions())

class GraphsHandler(RequestHandler):
    def get(self):
        with Database() as db:
            accounts = db.get_accounts()
            transactions=db.get_transactions()
            self.render("server/graphs.html")

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
                    account = None
                self.write(json.dumps([(date.isoformat(), label, description, float(amount), account_id) for id, date, label, description, amount, account_id in db.get_transactions(account)]))
    def post(self, request):
        if request=='transaction_category':
            print dir(self)
            self.write("OK")



if __name__ == "__main__":
    handlers = [
                (r'/static/(.*)', StaticFileHandler, {'path': 'server/'}),
                (r'/api/(.*)', APIHandler),
                (r'/', HomeHandler),
                (r'/categories', CategoriesHandler),
                (r'/graphs', GraphsHandler)
                ]
    application = Application(handlers)
    application.listen(8888)
    IOLoop.current().start()