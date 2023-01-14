import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

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
items = table.find_all('li', attrs={'class': 's-item s-item__pl-on-bottom'})

result = []
for item in items:
    title = item.find('div', attrs={'class': 's-item__title'}).text
    price = item.find('span', attrs={'class': 's-item__price'}).text
    location = item.find('span', attrs={'class': 's-item__location s-item__itemLocation'}).text

    try:
        review = item.find('span', attrs={'class': 's-item__reviews-count'}).find('span').text
    except AttributeError:
        review = 'No review yet'

    data_dict = {
        'Product name': title,
        'Price': price,
        'Location': location,
        'Review': review
    }
    result.append(data_dict)

try:
    os.mkdir('results')
except FileExistsError:
    pass

df = pd.DataFrame(result)

df.to_json('results/iphone.json', orient='records')
df.to_csv('results/iphone.csv', index=False)
df.to_excel('results/iphone.xlsx', index=False)