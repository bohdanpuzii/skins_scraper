import csv
import market_csgo
import steam

file_name = '20220917-145535.csv'
output_file_name = f'{file_name.split(".")[0]}_output.csv'
input_file = open(file_name)
output_file = open(output_file_name, 'a')
csv_reader = csv.reader(input_file, delimiter=',')
csv_writer = csv.writer(output_file)
csv_writer.writerow(['item', 'dmarket_price', 'market_csgo_current', 'highest_autobuy', 'average_sell_price', 'steam_lowest_price', 'steam_avg_price'])

for row in csv_reader:
    driver = market_csgo.get_driver(row[0])
    market_csgo_data = market_csgo.collect_data(driver)
    row.append(market_csgo_data['current_lowest'])
    row.append(market_csgo_data['lowest_request'])
    row.append(market_csgo_data['average'])
    steam_data = steam.get_item_data(row[0])
    if steam_data is not None and steam_data['success']:
        try:
            row.append(steam_data['lowest_price'].strip('$'))
            row.append(steam_data['median_price'].strip('$'))
        except:
            print(steam_data)
    #if row[1] > row[3] or row[1] > row[6]
    csv_writer.writerow(row)