import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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

driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7708&PageSize=96")
# driver.implicitly_wait(5)


def newegg():
    more_items = True
    while more_items:
        grab_items()
        more_items = next_page()


def grab_items():
    all_items = driver.find_elements(By.CLASS_NAME, 'item-container')
    for item in all_items:
        try:
            item.find_element(By.CLASS_NAME, 'item-sponsored-box')
            print("Sponsored item skipped...")
        except NoSuchElementException:
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


def next_page():
    page_index = driver.find_element(By.CLASS_NAME, 'list-tool-pagination-text').text.split(' ')[1]
    current_page = page_index.split('/')[0]
    total_pages = page_index.split('/')[1]
    print(current_page)
    if current_page != total_pages:
        driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/section/div/div/div[2]/div/div/div[2]/'
                                      'div[2]/div/div[1]/div[4]/div/div/div[11]/button').click()
        return True
    return False


newegg()

# close chromedriver
driver.quit()

print(f"TIME: {datetime.now() - start_time}")
