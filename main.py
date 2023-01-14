import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.ebay.com/sch/i.html?'

search = input('product search: ')


def send_req(page):
    params = {
        '_from': 'R40',
        '_nkw': search,
        '_sacat': '0',
        '_pgn': page,
    }

    req = requests.get(url, params=params)
    soup = BeautifulSoup(req.text, 'html.parser')

    table = soup.find('ul', attrs={'class': 'srp-results srp-list clearfix'})
    items = table.findAll('li', attrs={'class': 's-item s-item__pl-on-bottom'})

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
    return result


def extract_data(res, filename):
    try:
        os.mkdir('results')
    except FileExistsError:
        pass

    df = pd.DataFrame(res)

    df.to_json(f'results/{filename}.json', orient='records')
    df.to_csv(f'results/{filename}.csv', index=False)
    df.to_excel(f'results/{filename}.xlsx', index=False)


if __name__ == '__main__':
    data = send_req(str(1))
    extract_data(data, search)
