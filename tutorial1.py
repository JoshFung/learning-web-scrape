import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# IMPORT TO TIME SCRIPT
from datetime import datetime
start_time = datetime.now()

# guide im following: https://www.youtube.com/watch?v=j7VZsCCnptM

service = Service(executable_path=ChromeDriverManager().install())
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.newegg.ca/d/Best-Sellers/Desktop-Graphics-Cards/s/ID-48")
# driver.implicitly_wait(5)


def grab_items():
    all_items = driver.find_elements(By.CLASS_NAME, 'item-container')
    for item in all_items:
        item_details(item)


def item_details(item):
    item_title = item.find_element(By.CLASS_NAME, 'item-title').text
    item_normal_price = item.find_element(By.CLASS_NAME, 'price-was').text
    if item_normal_price == '':
        item_normal_price = item.find_element(By.CLASS_NAME, 'price-current').text
        item_sale_price = ''
    else:
        item_sale_price = item.find_element(By.CLASS_NAME, 'price-current').text

    item_shipping = item.find_element(By.CLASS_NAME, 'price-ship').text.split(' ')[0]
    print(f"ITEM: {item_title} -- "
          f"NORMAL PRICE: {item_normal_price} -- "
          f"SALE PRICE: {item_sale_price} -- "
          f"SHIPPING: {item_shipping}")


grab_items()

driver.quit()

print(f"TIME: {datetime.now()-start_time}")
