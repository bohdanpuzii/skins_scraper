import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup

only_weapons = True


def get_driver(start_price: float, end_price: float) -> webdriver.Chrome:
    url = f'https://dmarket.com/ru/ingame-items/item-list/csgo-skins?cheapestBySteamAnalyst=true&price-to={end_price}&price-from={start_price}'
    if only_weapons:
        url += '&exterior=all'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    return driver


def close_popups(driver: webdriver.Chrome,
                popup_x_xpath='//*[@id="mat-dialog-0"]/onboarding-dialog/div/div[1]/div/button',
                 not_today_button_xpath='//*[@id="onesignal-slidedown-cancel-button"]',) -> None:
    driver.implicitly_wait(5)
    try:
        driver.find_element(By.XPATH, popup_x_xpath).click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, not_today_button_xpath).click()
    except:
        pass
    driver.find_element(By.XPATH,
                        '/html/body/app-root/mat-sidenav-container/mat-sidenav-content/exchange/div/div/market-side/div/filters/div/div/filters-area/div/div[2]/dm-advanced-filters/dm-autocomplete-filter/div/autocomplete-option/autocomplete-link/a/span').click()
    time.sleep(2)


def sort_by_discount(dmarket_driver: webdriver.Chrome,
                     sort_bar_xpath='/html/body/app-root/mat-sidenav-container/mat-sidenav-content/exchange/div/div/market-side/div/filters/div/div/div[4]/sort-items/div/div',
                     discount_button_xpath='//*[@id="mat-menu-panel-0"]/div/button[3]') -> None:
    dmarket_driver.find_element(By.XPATH, sort_bar_xpath).click()
    dmarket_driver.find_element(By.XPATH, discount_button_xpath).click()
    time.sleep(2)


def get_items(driver: webdriver.Chrome, csv_file, items_selector='asset-card.c-asset.c-asset--steam.ng-star-inserted'):
    writer = csv.writer(csv_file)
    for item in driver.find_elements(By.CSS_SELECTOR, items_selector):
        html = item.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        name = validate_item_name(soup.select('img', {'class': 'c-asset__img'})[-1]['alt'])
        if soup.find('price'):
            price = soup.find('price').text
            writer.writerow([name, price])
        else:
            pass


def validate_item_name(name):
    return name.replace('|', '').strip(' ')
