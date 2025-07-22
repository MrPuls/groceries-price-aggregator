import csv

import requests
from bs4 import BeautifulSoup

base_url = 'https://silpo.ua/category/frukty-ovochi-4788'
results = []

# TODO: refactor and parallelize, painfully slow now and it's only one page

def parse(url, result_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    item_list = soup.find('div', class_='products-list')
    category = soup.find('h1', class_='catalog__products-title').get_text(strip=True)
    page = soup.find('a', class_='pagination-item--current').get_text(strip=True)

    for item in item_list.find_all('div', class_='products-list__item'):
        name = item.find('h3', class_='product-card__title')
        price = item.find('div', class_='product-card-price__displayPrice')
        result_list.append({
        'name': name.get_text(strip=True) if name is not None else None,
        'price': price.get_text(strip=True) if price is not None else None,
        'category': category,
        'page': page,
        'ref': url + item.find('a', class_='product-card__link').get('href')
        })

    next_page = soup.find('a', class_='pagination-item--next-page') or soup.find('div', class_='pagination__items').find_all('a', class_='pagination-item')[-1]
    next_page_ref = next_page.get('href')
    current_page = response.url.split('/')[-1]
    print(f'current_page: {current_page}')
    if next_page_ref[-3:] != response.url[-3:]:
        return parse(base_url + '?' + next_page_ref.split('?')[1], result_list)
    return result_list

res = parse(base_url, results)

with open('silpo.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'price', 'category', 'page', 'ref']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(res)