from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from sigsaur_webscrap import get_sigsauer_product_list
import sys
import sched, time
import smtplib
from email.message import EmailMessage
import threading
import os
import json

with open('config.json', 'r') as f:
    config = json.load(f)

# TODO: improve logic to make this custom with flags
# TODO: pass in through variables
FROM_USER_NAME = config['from_email_address']
FROM_EMAIL_PASSWORD = config['from_email_password']
TO_USER_NAME = config['to_email']
CHROME_DRIVER_PATH = config['chrome_driver_path']

# LOGIC for Chrome Driver set-up
chrome_driver_parth = os.path.dirname('/usr/bin/chromedriver')
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(FROM_USER_NAME, FROM_EMAIL_PASSWORD)
except Exception as e:
    print(e)
    exit(e)

known_sigsaur_instock = [0]

def main():
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=chrome_options)
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

# display = Display(visible=0, size=(800, 600))
# display.start()

scheduler = sched.scheduler(time.time, time.sleep)
print ('START:', time.time())
try:
    while True:
        scheduler.enter(5, 1, main,())
        scheduler.run()
except Exception as e:
    print(e)
    server.quit()
