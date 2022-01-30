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
    item_list = []
    while more_items:

        # TODO: first delay
        # sleep(randint(1, 5))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        get_all_items(soup, item_list)
        more_items = next_page()

    df = pd.DataFrame(item_list,
                      columns=['Store', 'Item', 'Brand', 'Normal Price', 'Sale Price', 'Rating', 'Shipping',
                               'Promo', 'Out of Stock'])
    df.to_csv('out.csv')


def get_all_items(soup, entries):
    all_items = soup.find_all('div', {'class': 'item-container'})

    for item in all_items:
        if item.find('div', {'class': 'item-sponsored-box'}) is not None:
            print("Sponsored item skipped...")
        else:
            item_entry = item_details(item)
            entries.append(item_entry)


def get_name(item, entry):
    item_name = item.find('a', {'class': 'item-title'}).text
    entry.update({'Item': item_name})


def get_brand(item, entry):
    item_brand = item.find('a', {'class': 'item-brand'})
    if item_brand is not None:
        item_brand = item_brand.find('img')['title']
    entry.update({'Brand': item_brand})


def get_shipping(item, entry):
    item_shipping = item.find('li', {'class': 'price-ship'}).getText().partition(" ")[0]
    entry.update({'Shipping': item_shipping})


def get_price(item, entry):
    item_normal_price = item.find('li', {'class': 'price-was'})
    # not on sale (empty array)
    if item_normal_price is None or item_normal_price.getText() == '':
        item_normal_price = item.find('li', {'class': 'price-current'}).getText()
        item_normal_price = item_normal_price.split()[0] if item_normal_price != '' else False
    else:
        item_normal_price = item_normal_price.getText().split()[0]
        item_sale_price = item.find('li', {'class': 'price-current'}).getText().split()[0]
        entry.update({'Sale Price': item_sale_price})
    entry.update({'Normal Price': item_normal_price})


def get_rating(item, entry):
    item_rating = item.find('i', {'class': 'rating'})
    if item_rating is not None:
        item_rating = item_rating['aria-label'].split(' ')[1]
        num_ratings = item.find('span', {'class': 'item-rating-num'}).getText().strip('()')
        entry.update({'Rating': item_rating + ' (' + num_ratings + ')'})


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
