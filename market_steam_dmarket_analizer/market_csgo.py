import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def get_driver(item_name) -> webdriver.Chrome:
    url = f'https://market.csgo.com/?t=all&search={item_name}'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, 'span.sorterby:nth-of-type(3)').click()
    time.sleep(1)
    return driver


def collect_data(driver: webdriver.Chrome, sort_selector='span.sorterby'):
    driver.find_element(By.CSS_SELECTOR, sort_selector).click()
    driver.find_element(By.CSS_SELECTOR, 'div.name').click()
    data = {}
    take_elem_by_selector(driver, data, 'current_lowest', 'div.ip-bestprice')
    take_elem_by_selector(driver, data, 'lowest_request', 'div:nth-of-type(6) div:nth-of-type(2) b')
    take_elem_by_selector(driver, data, 'average', 'div.rectanglestat:nth-of-type(3)')
    return data


def take_elem_by_selector(driver: webdriver.Chrome, data: dict, key: str, css_selector: str):
    try:
        data[key] = driver.find_element(By.CSS_SELECTOR, css_selector).text
    except:
        data[key] = 'No data'
