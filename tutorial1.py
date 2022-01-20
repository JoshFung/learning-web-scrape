import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# os.environ['PATH'] += r"D:/Programming/PycharmProjects/SeleniumDrivers/chromedriver.exe"
driver = webdriver.Chrome("D:/Programming/PycharmProjects/SeleniumDrivers/chromedriver.exe")

driver.get("https://www.memoryexpress.com/Category/VideoCards")

item_container = driver.find_element(By.CLASS_NAME, 'c-shca-icon-item_body-name')
print(item_container)