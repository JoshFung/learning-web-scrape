import pandas as pd
from bs4 import BeautifulSoup
from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from dotenv import load_dotenv
from random import randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import re

# ------------------------------------------------------------------------
# # TODO: Temporary Service() while Chromedriverv103 is broken
# # service = Service(executable_path=ChromeDriverManager().install())
# service = Service(executable_path=r"/Users/joshfung/Documents/PyCharm/learning-web-scrape/chromedriver")
#
# chrome_options = Options()
# # TODO: Remove when switching off beta of Chrome and Chromedriver
# chrome_options.binary_location = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"
# chrome_options.page_load_strategy = 'normal'
# driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7708&PageSize=96")
# # driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48/Page-7?Tid=7708&PageSize=96")
# ------------------------------------------------------------------------


app = Celery()
app.conf.beat_schedule = {
    # executes every 10 minute
    'scraping-task-ten-min': {
        'task': 'script.scrape',
        'schedule': crontab(minute='*/10')
    }
}


@app.task
def scrape():
    load_dotenv()

    # service = Service(executable_path=ChromeDriverManager().install())
    service = Service(executable_path=os.getenv("CHROMEDRIVER_PATH"))

    chrome_options = Options()
    # TODO: Remove when switching off beta of Chrome and Chromedriver
    chrome_options.binary_location = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"
    chrome_options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7708&PageSize=96")
    # driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48/Page-7?Tid=7708&PageSize=96")

    newegg(driver)

    driver.close()
    driver.quit()


@app.task
def newegg(driver):
    current_page = 1
    total_pages = find_pages(driver)
    item_list = []
    while current_page <= total_pages :

        # TODO: first delay
        sleep(randint(1, 5))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        get_all_items(soup, item_list)
        next_page(driver)

        # TODO: remove this eventually
        print(current_page)

        current_page += 1

    df = pd.DataFrame(item_list,
                      columns=['Store', 'Item', 'Brand', 'Normal Price', 'Sale Price', 'Rating', 'Shipping',
                               'Promo', 'Out of Stock'])
    if not os.path.exists('data'):
        os.mkdir('data')
    # df.to_csv(fr'data/out-{datetime.now().strftime("%Y%m%d-%H%M%S")}.csv')
    df.to_json(fr'data/out-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')


@app.task
def get_all_items(soup, entries):
    all_items = soup.find_all('div', {'class': 'item-container'})

    for item in all_items:
        if item.find('div', {'class': 'item-sponsored-box'}) is not None:
            print("Sponsored item skipped...")
        else:
            item_entry = item_details(item)
            entries.append(item_entry)


@app.task
def get_name(item, entry):
    item_name = item.find('a', {'class': 'item-title'}).text
    entry.update({'Item': item_name})


@app.task
def get_brand(item, entry):
    item_brand = item.find('a', {'class': 'item-brand'})
    if item_brand is not None:
        item_brand = item_brand.find('img')['title']
    entry.update({'Brand': item_brand})


@app.task
def get_shipping(item, entry):
    item_shipping = item.find('li', {'class': 'price-ship'}).getText().partition(" ")[0]
    entry.update({'Shipping': item_shipping})


@app.task
def extract_num(string):
    no_commas = string.replace(",", "")
    filtered_string = re.findall(r"\d+\.\d+", no_commas)
    return filtered_string[0]


@app.task
def get_price(item, entry):
    was_price = item.find('li', {'class': 'price-was'}).getText()
    current_price = item.find('li', {'class': 'price-current'}).getText()

    if was_price != '' and current_price != '':
        normal_price = extract_num(was_price)
        sale_price = extract_num(current_price)
    elif current_price != '':
        normal_price = extract_num(current_price)
        sale_price = None
    elif was_price != '':
        normal_price = extract_num(was_price)
        sale_price = None
    else:
        normal_price = None
        sale_price = None
    entry.update({'Normal Price': normal_price})
    entry.update({'Sale Price': sale_price})


@app.task
def get_rating(item, entry):
    item_rating = item.find('i', {'class': 'rating'})
    if item_rating is not None:
        item_rating = item_rating['aria-label'].split(' ')[1]
        num_ratings = item.find('span', {'class': 'item-rating-num'}).getText().strip('()')
        entry.update({'Rating': item_rating + ' (' + num_ratings + ')'})


@app.task
def get_promo(item, entry):
    item_promo = item.find('p', {'class': 'item-promo'})
    if item_promo is not None:
        item_promo = item_promo.getText()
        if item_promo == "OUT OF STOCK":
            entry.update({'Out of Stock': 'True'})
        else:
            entry.update({'Promo': item_promo})
            entry.update({'Out of Stock': 'False'})
    else:
        entry.update({'Out of Stock': 'False'})


@app.task
def item_details(item):
    item_entry = {}
    item_entry.update({'Store': 'Newegg'})
    get_name(item, item_entry)
    get_brand(item, item_entry)
    get_shipping(item, item_entry)
    get_price(item, item_entry)
    get_rating(item, item_entry)
    get_promo(item, item_entry)
    return item_entry


@app.task
def find_pages(driver):
    page_index = driver.find_element(By.CLASS_NAME, 'list-tool-pagination-text').text.split(' ')[1]
    # current_page = page_index.split('/')[0]
    return int(page_index.split('/')[1])


@app.task
def next_page(driver):
    # make sure it loads in (otherwise it can throw an error)
    try:
        WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-tool-pagination-text')))
    except TimeoutException:
        driver.quit()

    # TODO: second delay
    sleep(randint(1, 5))

    driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/section/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div[4]/div/div/div[11]/button').click()
