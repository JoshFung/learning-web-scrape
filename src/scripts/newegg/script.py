import pandas as pd
from bs4 import BeautifulSoup
from random import randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3 as sql
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager

# TODO: remove this -- IMPORT TO TIME SCRIPT
from datetime import datetime

start_time = datetime.now()

# ------------------------------------------------------------------------
service = Service(executable_path=ChromeDriverManager().install())
chrome_options = Options()
chrome_options.page_load_strategy = 'normal'
driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.get("https://www.newegg.ca/p/pl?PageSize=60&N=100007708")
driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7708&PageSize=96")
# ------------------------------------------------------------------------


def newegg():
    more_items = True
    conn = sql.connect('src/databases/items.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE items (store TEXT, item TEXT, brand TEXT, shipping TEXT, normal_price, sale_price, rating, promo, out_of_stock)
        """)
    while more_items:

        # TODO: first delay
        # sleep(randint(1, 5))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        get_all_items(soup, c)
        more_items = next_page()
    conn.commit()


def get_all_items(soup, cursor):
    all_items = soup.find_all('div', {'class': 'item-container'})

    for item in all_items:
        if item.find('div', {'class': 'item-sponsored-box'}) is not None:
            print("Sponsored item skipped...")
        else:
            create_record(item, cursor)


def get_name(item):
    return item.find('a', {'class': 'item-title'}).text
    

def get_brand(item):
    brand = item.find('a', {'class': 'item-brand'})
    if brand is not None:
        brand = brand.find('img')['title']
    return brand


def get_shipping(item):
    shipping = item.find('li', {'class': 'price-ship'}).getText().partition(" ")[0].strip('$ ')
    if shipping in ['Free', 'Special']:
        shipping = 0
    elif shipping == '':
        return ''
    return float(shipping)
    

def get_price(item):
    normal_price = item.find('li', {'class': 'price-was'})
    # not on sale (empty array)
    if normal_price is None or normal_price.getText() == '':
        normal_price = item.find('li', {'class': 'price-current'}).getText()
        normal_price = normal_price.split()[0] if normal_price != '' else False
        return (normal_price, '')
    normal_price = normal_price.getText().split()[0]
    sale_price = item.find('li', {'class': 'price-current'}).getText()
    sale_price = sale_price.split()[0] if sale_price != '' else False
    return (normal_price, sale_price)


def get_rating(item):
    item_rating = item.find('i', {'class': 'rating'})
    if item_rating is not None:
        item_rating = item_rating['aria-label'].split(' ')[1]
        num_ratings = item.find('span', {'class': 'item-rating-num'}).getText().strip('()')
        return (item_rating + ' (' + num_ratings + ')')


def get_promo(item):
    promo = item.find('p', {'class': 'item-promo'})
    if promo is not None:
        promo = promo.getText()
        if promo == "OUT OF STOCK":
            return ('', 'Yes')
        else:
            return (promo, 'No')
    else:
        return ('', 'No')


def create_record(item, cursor):
    store = 'Newegg'
    name = get_name(item)
    brand = get_brand(item)
    shipping = get_shipping(item)
    prices = get_price(item)
    normal_price = prices[0]
    sale_price = prices[1]
    rating = get_rating(item)
    promo = get_promo(item)
    out_of_stock = promo[1]
    promo = promo[0]
    cursor.execute('''
    INSERT INTO items (store, item, brand, shipping, normal_price, sale_price, rating, promo, out_of_stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
    (store, name, brand, shipping, normal_price, sale_price, rating, promo, out_of_stock))


def next_page():
    # make sure it loads in (otherwise it can throw an error)
    try:
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-tool-pagination-text')))
    except TimeoutException:
        driver.quit()

    page_index = driver.find_element(By.CLASS_NAME, 'list-tool-pagination-text').text.split(' ')[1]
    current_page = page_index.split('/')[0]
    total_pages = page_index.split('/')[1]

    # TODO: remove this eventually
    print(current_page)

    # TODO: second delay
    # sleep(randint(1, 5))

    if current_page != total_pages:
        driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/section/div[1]/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div/div[11]/button').click()
        return True
    return False


newegg()

# close chromedriver
driver.quit()

# TODO: remove this
print(f"TIME: {datetime.now() - start_time}")
