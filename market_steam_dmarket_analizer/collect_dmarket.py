import dmarket
import time

f = open(f'{time.strftime("%Y%m%d-%H%M%S")}.csv', 'a')

start_price = 0.01
end_price = 0.02

while end_price != 1:
    driver = dmarket.get_driver(start_price, end_price)
    dmarket.close_popups(driver)
    dmarket.get_items(driver, f)
    end_price += 0.02
    start_price += 0.02
f.close()
