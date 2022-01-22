import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# guide im following: https://www.youtube.com/watch?v=j7VZsCCnptM

driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'])

driver.get("https://www.newegg.ca/d/Best-Sellers/Desktop-Graphics-Cards/s/ID-48")

item_container = driver.find_element(By.CLASS_NAME, 'item-title')
print(f"{item_container.text}")