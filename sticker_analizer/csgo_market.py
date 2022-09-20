import time

import requests


from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


NO_DATA = 'No data'

STICKER_ID = '294'
AGENT_ID = '22697803'
PINS_ID = '665673'


def get_driver_page(page: int) -> webdriver.Chrome:
    url = f'https://market.csgo.com/?s=pop&t={PINS_ID}&rs=1;500000&p={page}'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver


def get_driver_item(item_href: str) -> webdriver.Chrome:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(item_href)
    return driver


def get_total_pages(driver: webdriver.Chrome):
    return int(driver.find_element(By.ID, 'total_pages').text)


def iterate_on_pages(page_count: int):
    for page in range(1, page_count):
        print(f'{page=}')
        driver = get_driver_page(page)
        items = driver.find_elements(By.CSS_SELECTOR, '#applications a')
        for item in items:
            item_page = get_driver_item(item.get_attribute('href'))
            get_item_data(item_page)


def get_item_data(item_page: webdriver.Chrome):
    name = take_elem_by_selector(item_page, 'h1')
    current_price = take_elem_by_selector(item_page, 'div.ip-bestprice')
    requests_count = take_elem_by_selector(item_page, 'div:nth-of-type(5) div.rectanglestat:nth-of-type(1) b')
    highest_request = take_elem_by_selector(item_page, 'div:nth-of-type(6) div:nth-of-type(2) b')
    # steam_data = get_steam_data(name)
    # if highest_request != NO_DATA and steam_data[0] != NO_DATA and float(steam_data[0]) < float(highest_request):
    #     print(f'{name=} {current_price=}, {requests_count=}, {highest_request=} stem_lowest={steam_data[0]}')
    steam_price = get_steam_price(get_steam_page(name))
    if highest_request != NO_DATA and steam_price != NO_DATA and float(highest_request) > float(steam_price):
        print(f'{name=} {current_price=}, {requests_count=}, {highest_request=} {steam_price=}')


def take_elem_by_selector(item_page: webdriver.Chrome, css_selector: str):
    try:
        return item_page.find_element(By.CSS_SELECTOR, css_selector).text
    except:
        return NO_DATA


def get_steam_page(item_name: str) -> webdriver.Chrome:
    url = f'https://steamcommunity.com/market/search?q={item_name}'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    print(driver)
    time.sleep(1)
    return driver


def get_steam_price(item_page: webdriver.Chrome):
    try:
        return item_page.find_element(By.XPATH, '//*[@id="result_0"]/div[1]/div[2]/span[1]/span[1]').text.strip('$').replace('USD', '').replace(',', '')
    except:
        time.sleep(100)
        return NO_DATA


def get_steam_data(item_name: str):
    url = f'https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=' \
          f'{item_name}'
    response = requests.get(url)
    try:
        return response.json()['lowest_price'].strip('$').replace(',', '') \
            if 'median_price' in response.json().keys() else NO_DATA
    except:
        return NO_DATA