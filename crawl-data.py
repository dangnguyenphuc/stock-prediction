import numpy as np
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import random
import pandas as pd
import os
import time

def get_date(date):
    return datedate[-2:-1]+datedate[5:6]+datedate[2:3]

# Set the download directory path to project folder
download_directory = "/Users/phucdang/Documents/dangnguyen/Document/DE/project/"

# Set up Firefox options
firefox_options = Options()
firefox_options.set_preference("browser.download.folderList", 2)
firefox_options.set_preference("browser.download.dir", download_directory)
firefox_options.set_preference("browser.download.useDownloadDir", True)
firefox_options.set_preference("browser.download.viewableInternally.enabledTypes", "")
firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")


url = 'https://vn.investing.com'
username = 'mongtuyenftu2@gmail.com'
password = 'ThaiNgoc_2002'
stock = 'VN30'
startdate = '2013-10-03'
enddate = '2023-10-03'


driver = webdriver.Firefox(options=firefox_options)
driver.get(url + '/indices/')



login = driver.find_elements(By.CSS_SELECTOR, '.login')
login[0].click()

username_input = driver.find_element(By.CSS_SELECTOR, '#loginFormUser_email')
# Enter a new date value into the input field (replace 'yyyy-mm-dd' with your desired date)
username_input.send_keys(username)

password_input = driver.find_element(By.CSS_SELECTOR, '#loginForm_password')
# Enter a new date value into the input field (replace 'yyyy-mm-dd' with your desired date)
password_input.send_keys(password)

enter = driver.find_elements(By.CSS_SELECTOR, 'a.newButton:nth-child(4)')
enter[0].click()

main_link1 = driver.find_elements(By.CSS_SELECTOR, '#realTimeStockMarkets h2 a')
main_link2 = driver.find_elements(By.CSS_SELECTOR, '#realTimeStockMarkets h3 a')

links = []
for link in main_link1:
    links += [link.get_attribute('href')]
for link in main_link2:
    links += [link.get_attribute('href')]


######################################
print(links)

'''
Output:
['https://vn.investing.com/indices/vietnam-indices',
 'https://vn.investing.com/indices/major-indices',
 'https://vn.investing.com/indices/americas-indices',
 'https://vn.investing.com/indices/european-indices',
 'https://vn.investing.com/indices/asian-pacific-indices']
'''
######################################

# Then we can get vietnam-indices:
vietnam_indices_link = links[0]

# Access the link specified by the href
driver.get(vietnam_indices_link)


# Inspect on web :)
row_class = '.dynamic-table_col-name__tHB5C .datatable_cell__wrapper__4bnlr .inv-link.bold.datatable_cell--name__link__2xqgx'

vietname_indices_element = driver.find_elements(By.CSS_SELECTOR, row_class)

vietname_indices_link = [link.get_attribute('href') for link in vietname_indices_element]


######################################
print(vietname_indices_link)
'''
Output:
['https://vn.investing.com/indices/hnx-30',
 'https://vn.investing.com/indices/vn',
 'https://vn.investing.com/indices/vn-30',
 'https://vn.investing.com/indices/ftse-vietnam',
 'https://vn.investing.com/indices/ftse-vietnam-all',
 'https://vn.investing.com/indices/hnx',
 'https://vn.investing.com/indices/vn100']
'''
######################################

# we can get all but just getting vn30 is enough :)
stock_link = vietname_indices_link[2]

driver.get(stock_link)


# can do same for other stock indices
historical_path = '/html/body/div/div[2]/div[2]/div[2]/div[1]/nav/div[2]/ul/li[3]/a'
historical_elem = driver.find_elements(By.XPATH, historical_path)
historical_link = historical_elem[0].get_attribute('href')
driver.get(historical_link)




# After accessing historical_link then:

# click the calendar
calendar_elem = driver.find_elements(By.CSS_SELECTOR, '.px-\[14px\]')
calendar_elem[0].click()

# then there will be 2 date input fields 

##### INPUT 1
date_input1 = driver.find_element(By.CSS_SELECTOR, 'div.NativeDateInputV2_root__uAIu0:nth-child(1) > input:nth-child(2)')
# Enter a new date value into the input field (replace 'yyyy-mm-dd' with your desired date)
date_input1.send_keys(startdate)
#########################


##### INPUT 2
date_input2 = driver.find_element(By.CSS_SELECTOR, 'div.NativeDateInputV2_root__uAIu0:nth-child(2) > input:nth-child(2)')
# Enter a new date value into the input field (replace 'yyyy-mm-dd' with your desired date)
date_input2.send_keys(enddate)
#########################

#Then click "Ap Dung" :v
enter_elem = driver.find_elements(By.CSS_SELECTOR, 'div.py-2\.5:nth-child(2)')
enter_elem[0].click()

# then click "Tai xuong" :v
download_elem = driver.find_elements(By.CSS_SELECTOR, '.download-data_csv-link__2ffbv')
driver.get(download_elem[0].get_attribute('href'))
driver.close()

csv_files = [f for f in os.listdir(download_directory) if f.endswith(".csv")]

# Check if there are any CSV files in the folder
if csv_files:
    # Get the full path for each CSV file
    csv_file_paths = [os.path.join(download_directory, file) for file in csv_files]

    # Get the newest CSV file based on creation time
    newest_csv = max(csv_file_paths, key=os.path.getctime)
    os.rename(newest_csv, download_directory + stock + '_' +get_date(startdate) + '_' +get_date(enddate))