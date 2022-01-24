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

# guide im following: https://www.youtube.com/watch?v=j7VZsCCnptM

service = Service(executable_path=ChromeDriverManager().install())
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.newegg.ca/Desktop-Graphics-Cards/SubCategory/ID-48?Tid=7708&PageSize=96")


def newegg():
    more_items = True
    while more_items:

        # TODO: first delay
        sleep(randint(1, 5))

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        grab_items(soup)
        more_items = next_page()


def grab_items(soup):
    # all_items = driver.find_elements(By.CLASS_NAME, 'item-container')
    all_items = soup.find_all('div', {'class': 'item-container'})

    for item in all_items:
        # try:
        #     item.find_element(By.CLASS_NAME, 'item-sponsored-box')
        #     print("Sponsored item skipped...")
        # except NoSuchElementException:
        #     item_details(item)
        if item.find('div', {'class': 'item-sponsored-box'}) is not None:
            print("Sponsored item skipped...")
        else:
            item_details(item)


def item_details(item):

    item_title = item.find('a', {'class': 'item-title'}).text
    item_shipping = item.find('li', {'class': 'price-ship'}).text

    item_normal_price = item.find('li', {'class': 'price-was'}).text
    if item_normal_price is not None:
        item_sale_price = item.find('li', {'class': 'price-current'}).text
        item_percentage_saved = item.find('li', {'class': 'price-save'}).text
    else:
        item_normal_price = item.find('li', {'class': 'price-current'}).text

    item_rating = item.find('i', {'class': 'rating'})
    if item_rating is not None:
        item_rating = item_rating['aria-label'].split(' ')[1]
        num_ratings = item.find('span', {'class': 'item-rating-num'}).text.strip('()')
    else:
        item_rating = "no rating"
        num_ratings = "no ratings"

    # print(f'ITEM: {item_title} -- '
    #       f'NORMAL PRICE: {item_normal_price} -- '
    #       f'{f"SALE PRICE: {item_sale_price} --" if item_sale_price else ""} '
    #       f'SHIPPING: {item_shipping}')


def next_page():
    # make sure it loads in (otherwise it can throw an error)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-tool-pagination-text')))
    except TimeoutException:
        driver.quit()

    page_index = driver.find_element(By.CLASS_NAME, 'list-tool-pagination-text').text.split(' ')[1]
    current_page = page_index.split('/')[0]
    total_pages = page_index.split('/')[1]

    # TODO: remove this eventually
    print(current_page)

    # TODO: second delay
    sleep(randint(1, 5))

    if current_page != total_pages:
        driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/section/div/div/div[2]/div/div/div[2]/'
                                      'div[2]/div/div[1]/div[4]/div/div/div[11]/button').click()
        return True
    return False


newegg()

# close chromedriver
driver.quit()

# TODO: remove this
print(f"TIME: {datetime.now() - start_time}")
