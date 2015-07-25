import keyring
# Some env variables
PATH = '/Users/nicolas/'
DATA_PATH = PATH+'Data/bankscraper/'
# Database
DB_HOST = 'grislain.fr'
DB_USER = 'bankscraper'
DB_PASSWORD = keyring.get_password('fr.grislain.mysql.bankscraper', 'bankscraper')
DB_NAME = 'bankscraper'