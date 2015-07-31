import keyring
# Set database credentials
keyring.set_password('fr.grislain.mysql.bankscraper', 'bankscraper', raw_input('database password :'))
# Set bank credentials
keyring.set_password('fr.grislain.societegenerale.login', 'nicolas', raw_input('login de Nicolas :'))
keyring.set_password('fr.grislain.societegenerale.password', 'nicolas', raw_input('password :'))
keyring.set_password('fr.grislain.societegenerale.login', 'celine', raw_input('login de Celine :'))
keyring.set_password('fr.grislain.societegenerale.password', 'celine', raw_input('password :'))
