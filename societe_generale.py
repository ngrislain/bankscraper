import urllib
import webbrowser
import time
import thread
# Import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
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
    driver = webdriver.Firefox()
    driver.get(login_url)
    driver.find_element_by_id('codcli').send_keys(str(client_id))
    driver.find_element_by_id('button').click()
    # Wait for the login process to complete
    element = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/restitution/tel_telechargement.html"]')))
    print element

get_transactions()

