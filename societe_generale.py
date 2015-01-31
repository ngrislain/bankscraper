import urllib
import webbrowser
import time
import thread
from datetime import date, timedelta
# Import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

def login():
    url = 'https://particuliers.societegenerale.fr/'
    login_wait_time = 1
    # Test the login
    def test_login():
        url = 'https://particuliers.secure.societegenerale.fr/restitution/tel_telechargement.html'
        page = urllib.urlopen(url).read()
        if 'Votre session a expir&eacute;. Merci de bien vouloir vous identifier &agrave; nouveau.' in page:
            print 'Not logged in'
            return False
        else:
            print 'OK'
            return True
    # Login
    webbrowser.open(url)
    # Wait for login
    while not test_login():
        time.sleep(login_wait_time)
    

def get_transactions(client_id=30144911):
    # Shows the login invite
    login_url = 'https://particuliers.societegenerale.fr/'
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.panel.shown', True)
    profile.set_preference('browser.download.manager.showAlertOnStart', False)
    profile.set_preference('browser.download.manager.showAlertOnComplete', False)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-ecriture-txt')
    driver = webdriver.Firefox(profile)
    driver.get(login_url)
    codcli = str(client_id)
    driver.find_element_by_id('codcli').send_keys(codcli)
    driver.find_element_by_id('button').click()
    # Wait for the login process to complete
    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/restitution/tel_telechargement.html"]'))).click()
    # Select the account to download (current account)
    select = Select(driver.find_element_by_id('compte'))
    select.select_by_index(1) # Get the first element
    # Select the format
    Select(driver.find_element_by_name('logicielFull')).select_by_value('TSV')
    # Select the date range
    datedu = (date.today()-timedelta(days=180)).strftime('%d/%m/%Y')
    driver.find_element_by_name('datedu').send_keys(datedu)
    # Get the data
    driver.find_element_by_css_selector('a[href="javascript:telecharger(this)"]').click()

    
get_transactions()

