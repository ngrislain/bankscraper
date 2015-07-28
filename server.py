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
            self.render("server/categories.html", categories=db.get_categories(), transactions=db.get_transactions())

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
                # Getting account
                if len(self.get_arguments('account_id'))>0:
                    account_id = self.get_arguments('account_id')[0]
                elif len(self.get_arguments('account_label'))>0:
                    account_id = next(account[0] for account in db.get_accounts() if account[1]==self.get_arguments('account_label')[0])
                else:
                    account_id = None
                # Getting category
                if len(self.get_arguments('category_id'))>0:
                    category_id = self.get_arguments('category_id')[0]
                elif len(self.get_arguments('category_label'))>0:
                    category_id = next(category[0] for category in db.get_categories() if category[1]==self.get_arguments('category_label')[0])
                else:
                    category_id = None
                self.write(json.dumps([(date.isoformat(), label, description, float(amount), account_id, category) for id, date, label, description, amount, account_id, category in db.get_transactions(account_id, category_id)]))
        elif request=='transaction_category':
            with Database() as db:
                transaction = int(self.get_arguments('transaction')[0])
                if self.get_arguments('q')[0]=='insert':
                    category = int(self.get_arguments('category')[0])
                    db.insert_transaction_category(transaction, category)
                elif self.get_arguments('q')[0]=='delete':
                    db.delete_transaction_category(transaction)

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