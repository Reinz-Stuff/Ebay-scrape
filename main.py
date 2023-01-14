import requests
from bs4 import BeautifulSoup

url = 'https://www.ebay.com/sch/i.html?'

params = {
    '_from': 'R40',
    '_nkw': 'iphone',
    '_sacat': '0',
    '_pgn': '1',
}

req = requests.get(url, params=params)
soup = BeautifulSoup(req.text, 'html.parser')

table = soup.find('ul', attrs={'class': 'srp-results srp-list clearfix'})
title = table.findAll('div', attrs={'class': 's-item__title'})
for i in title:
    print(i.text)