import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


def get_driver(item_name) -> webdriver.Chrome:
    url = f'https://steamcommunity.com/market/search?q={item_name.replace("  ", " | ")}'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver


def get_item_data(item_name):
    url = f'https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=' \
          f'{item_name.replace("  ", " | ")}'
    response = requests.get(url)
    return response.json()