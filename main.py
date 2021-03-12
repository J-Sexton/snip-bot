from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from sigsaur_webscrap import get_sigsauer_product_list
import sched, time
import smtplib
from email.message import EmailMessage
import threading
import os
# TODO: improve logic to make this custom with flags
chrome_driver_parth = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
known_sigsaur_instock = [0]
FROM_USER_NAME = 'mister.cripto@gmail.com'
TO_USER_NAME = '7068472405@vtext.com'
#TODO: pass in through variables
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(FROM_USER_NAME, 'vems lhzg hucd zdlw')
except Exception as e:
    print(e)
    exit(e)


def main():
    driver = webdriver.Chrome(chrome_driver_parth, options=chrome_options)
    print(time.time())
    global known_sigsaur_instock
    sigsaur_instock = get_sigsauer_product_list('ammunition.html?caliber=1915%2C1917',driver)
    updated_stock = compare_knownstock_with_received_stock(sigsaur_instock)
    known_sigsaur_instock = sigsaur_instock
    if len(updated_stock) != 0:
        for i in sigsaur_instock:
            server.sendmail(FROM_USER_NAME, TO_USER_NAME, '\n'+i)
    else: 
        print('No instock changes detected, not sending')

def compare_knownstock_with_received_stock(current_stock):
    global known_sigsaur_instock
    stock_changes = []
    for item in current_stock:
        if item not in known_sigsaur_instock:
            stock_changes.append(item)
    return stock_changes

scheduler = sched.scheduler(time.time, time.sleep)
print ('START:', time.time())
try:
    while True:
        scheduler.enter(5, 1, main,())
        scheduler.run()
except Exception as e:
    print(e)
    server.quit()
