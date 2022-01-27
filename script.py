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
driver.get("https://www.newegg.ca/p/pl?PageSize=60&N=100007708")
# driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7708&PageSize=96")
# ------------------------------------------------------------------------
count = 0

item_list = []
entry = {}
entry.update({'Store': 'Newegg'})
entry.update({'Item': 'ASUS ROG Strix Radeon RX 590 8GB GDDR5 CrossFireX Support Video Card ROG-STRIX-RX590-8G-GAMING'})
entry.update({'Brand': 'ASUS'})
entry.update({'Normal Price': '$1,377.00'})
entry.update({'Sale Price': '$900.00'})
entry.update({'Rating': '5 / 40 ratings'})
entry.update({'Shipping': '$5.99'})
entry.update({'Promo': 'Xbox game pass for 1 month'})
entry.update({'Out of Stock': False})
# entry = {'Newegg', 'ASUS ROG Strix Radeon RX 590 8GB GDDR5 CrossFireX Support Video Card ROG-STRIX-RX590-8G-GAMING', 'ASUS',
#            '$1,377.00', '$900.00', '5 / 40 ratings', '$5.99', 'Xbox game pass for 1 month', False}
item_list.append(entry)
df = pd.DataFrame(item_list, columns=['Store', 'Item', 'Brand', 'Normal Price', 'Sale Price', 'Rating', 'Shipping', 'Promo',
                           'Out of Stock'])
df.to_csv('out.csv')


def newegg():
    more_items = True
    while more_items:

        # TODO: first delay
        # sleep(randint(1, 5))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        grab_items(soup)
        more_items = next_page()


def grab_items(soup):
    all_items = soup.find_all('div', {'class': 'item-container'})

    for item in all_items:
        global count
        count += 1
        if item.find('div', {'class': 'item-sponsored-box'}) is not None:
            print("Sponsored item skipped...")
        else:
            item_details(item)


def item_details(item):
    item_normal_price, item_sale_price, item_brand, item_rating, item_promo, item_shipping = (False,)*6

    # name
    item_title = item.find('a', {'class': 'item-title'}).text

    # shipping price
    item_shipping = item.find('li', {'class': 'price-ship'}).getText().partition(" ")[0]

    # brand
    item_brand = item.find('a', {'class': 'item-brand'})
    if item_brand is not None:
        item_brand = item_brand.find('img')['title']

    # normal price, sale price, and percentage saved
    item_normal_price = item.find('li', {'class': 'price-was'})
    # not on sale (empty array)
    if item_normal_price is None or item_normal_price.getText() == '':
        item_normal_price = item.find('li', {'class': 'price-current'}).getText()
        item_normal_price = item_normal_price.split()[0] if item_normal_price != '' else False
    else:
        item_normal_price = item_normal_price.getText().split()[0]
        item_sale_price = item.find('li', {'class': 'price-current'}).getText().split()[0]

    # rating and num of ratings
    item_rating = item.find('i', {'class': 'rating'})
    if item_rating is not None:
        item_rating = item_rating['aria-label'].split(' ')[1]
        num_ratings = item.find('span', {'class': 'item-rating-num'}).getText().strip('()')

    # promo and OOS
    out_of_stock = False
    item_promo = item.find('p', {'class': 'item-promo'})
    if item_promo == "OUT OF STOCK":
        item_promo = None
        out_of_stock = True
    elif item_promo is not None:
        item_promo = item_promo.getText()
#
#     print(f'ITEM: {item_title}\n'
#           f'    {f"NORMAL PRICE: {item_normal_price}" if item_normal_price else ""}\n'
#           f'    {f"SALE PRICE: {item_sale_price}" if item_sale_price else ""}\n'
#           f'    {f"RATING: {item_rating} OUT OF {num_ratings} RATINGS" if item_rating else ""}\n'
#           f'    {f"BRAND: {item_brand}" if item_brand else ""}\n'
#           f'    {f"SHIPPING: {item_shipping}" if item_shipping else ""}\n'
#           f'    {f"PROMO: {item_promo}" if item_promo else "" }\n'
#           f'    OUT OF STOCK: {out_of_stock}\n'
#           )
#
#
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
        # driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/section/div/div/div[2]/div/div/div[2]/'
        #                               'div[2]/div/div[1]/div[4]/div/div/div[11]/button').click()
        driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/section/div/div/div[2]/div/div/div/div[2]/div/div/'
                                      'div[3]/div/div/div[11]/button').click()
        return True
    return False


newegg()
print(count)

# close chromedriver
driver.quit()

# TODO: remove this
print(f"TIME: {datetime.now() - start_time}")
