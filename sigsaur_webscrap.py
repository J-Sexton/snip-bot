from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_sigsauer_product_list(keywords, driver):
    BASE_URL = 'http://www.sigsauer.com/'
    shop_url = BASE_URL + keywords
    r = driver.get(shop_url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="amasty-shopby-product-list"]/div[3]/ol'))
            )
    except Exception as e:
        print(e)
        driver.quit()
    elements = driver.find_elements_by_xpath('//*[@id="amasty-shopby-product-list"]/div[3]/ol/li')
    return check_product_list_for_available(elements,driver)
    
def check_product_list_for_available(items, driver):
    instock_items = []
    for i in items:
        item_text = i.text.split('\n',-1)
        if item_text[4] == 'ADD TO CART':
            if item_text[1] == 'New!':
                instock_items.append((item_text[2]+ ' : '+item_text[3]+ ' : '+ driver.current_url+' \n'))
            else:
                instock_items.append((item_text[1]+ ' : '+item_text[3]+ ' : '+ driver.current_url+' \n'))
    # quiting driver here, in future may need to keep around to execute a purchase
    driver.quit()
    return instock_items