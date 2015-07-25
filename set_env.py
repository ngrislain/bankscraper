import keyring
# Set database credentials
keyring.set_password('fr.grislain.mysql.bankscraper', 'bankscraper', '********')
# Set bank credentials
keyring.set_password('fr.grislain.societegenerale.login', 'nicolas', raw_input('\nlogin de Nicolas :'))
keyring.set_password('fr.grislain.societegenerale.password', 'nicolas', raw_input('\npassword :'))
keyring.set_password('fr.grislain.societegenerale.login', 'celine', raw_input('\nlogin de Celine :'))
keyring.set_password('fr.grislain.societegenerale.password', 'celine', raw_input('\npassword :'))
