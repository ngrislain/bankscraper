from database import Database

CURRENT_ACCOUNT = '0312500050278659'

with Database() as db:
    transactions = db.get_transactions(account_id=CURRENT_ACCOUNT)
    categories = db.get_categories()

with Database() as db:
    db.push_transaction_categories([(2969L, 10L), (724L, 1L), (725L, 1L), (3034L, 1L)])
    
for transaction in transactions:
    print transaction

# ((1L, 'alimentation', ''),
#  (2L, 'assurance', ''),
#  (3L, 'banque', ''),
#  (4L, '\xc3\xa9nergie', ''),
#  (5L, '\xc3\xa9pargne', ''),
#  (6L, 'garde', ''),
#  (7L, 'imp\xc3\xb4ts', ''),
#  (8L, 'kin\xc3\xa9', ''),
#  (9L, 'logement', ''),
#  (10L, 'loisirs', ''),
#  (12L, 'm\xc3\xa9nage', ''),
#  (11L, 'mobilier', ''),
#  (13L, 'salaires', ''),
#  (14L, 'sant\xc3\xa9', ''),
#  (16L, 't\xc3\xa9l\xc3\xa9com', ''),
#  (15L, 'transport', ''),
#  (17L, 'vacances', ''),
#  (18L, 'v\xc3\xaatements PC', ''),
#  (19L, 'v\xc3\xaatements PCT', ''))