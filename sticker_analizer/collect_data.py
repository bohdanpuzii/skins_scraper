import csgo_market


driver = csgo_market.get_driver_page(1)
page_count = csgo_market.get_total_pages(driver)
csgo_market.iterate_on_pages(page_count)
