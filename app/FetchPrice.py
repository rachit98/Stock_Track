import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from csv import writer
from datetime import date

url = 'https://www.moneycontrol.com/india/stockpricequote/'

with open('../files/stock_list.csv','r') as file:
    stock_symbols = file.read()
    stock_symbols = stock_symbols.splitlines()
    file.close()


for stocks in stock_symbols:
    stocks = stocks.split(',')

    stock_name = stocks[0]
    extended_url = stocks[1]
    stock_url = url + extended_url
    response = requests.get(stock_url,
                            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                                                   "like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    ltp = soup.find(id='nsecp').getText()
    day_low = soup.find(id='sp_low').getText()
    day_high = soup.find(id='sp_high').getText()
    overview = soup.find(id='stk_overview').getText().strip().splitlines()
    day_open = overview[1]
    prev_close = overview[5]
    volume = overview[10]
    today = date.today()
    day_open = Decimal(day_open.replace(',', ''))
    day_close = Decimal(ltp.replace(',', ''))
    day_high = Decimal(day_high.replace(',', ''))
    day_low = Decimal(day_low.replace(',', ''))
    volume = Decimal(volume.replace(',', ''))

    data = [today, day_open, day_high, day_low, day_close, volume]
    print(stock_name)
    print(data)

    with open('../files/stock_data/'+stock_name+'.csv', 'a+', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(data)
        file.close()

print('Fetch Completed.')
