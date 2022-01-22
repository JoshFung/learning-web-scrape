import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# guide im following: https://www.youtube.com/watch?v=j7VZsCCnptM

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.newegg.ca/d/Best-Sellers/Desktop-Graphics-Cards/s/ID-48")

item_container = driver.find_element(By.CLASS_NAME, 'item-title')
print(f"{item_container.text}")