from weboob.core import Weboob
from weboob.capabilities.bank import CapBank
w = Weboob()
w.load_backends(CapBank)
print list(w.iter_accounts())
acc = next(iter(w.iter_accounts()))
acc.balance
