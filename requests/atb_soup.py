import csv
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Accept': '*/*',
        'Accept-Encoding': 'utf-8',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Dest': 'empty',
        'Sec-GPC': '1',
        'TE': 'trailers',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.atbmarket.com',
        'Referer': 'https://www.atbmarket.com/',
    }

def get_categories():
    categories = []
    base_url = 'https://www.atbmarket.com'
    response = request.Request(base_url, headers=headers)
    soup = BeautifulSoup(request.urlopen(response).read(), 'lxml')
    menu = soup.find('ul', class_='category-menu')
    for category_ref in menu.find_all('li', class_='category-menu__item'):
        categories.append(base_url + category_ref.find('a').get('href'))
    return categories

def get_products(url, page=None):
    request_url = f'{url}?page={page}' if page else url
    print(f'getting products from: {request_url}')
    response = request.Request(request_url, headers=headers)

    soup = BeautifulSoup(request.urlopen(response).read(), 'lxml')
    results = []

    for item in soup.find('div', class_='catalog-list').find_all("article", class_='catalog-item'):
        results.append({
            'category': soup.find('h1', class_='page-title').get_text(strip=True),
            'name': item.find('div', class_='catalog-item__title').find('a').get_text(strip=True),
            'price': item.find('data', class_='product-price__top').get('value') +
                     ' ' +
                     item.find('abbr', class_='product-price__currency-abbr').get_text(strip=True),
            'ref': response.full_url + item.find('div', class_='catalog-item__title').find('a').get('href'),
        }
        )

    pagination = soup.find('ul', class_='product-pagination__list')
    if pagination:
        max_pages = pagination.find_all('li', class_='product-pagination__item')[-2].get_text(strip=True)
        next_page_ref = (pagination.find('li', class_='product-pagination__item active')
                         .find_next('li', class_='product-pagination__item')
                         .get_text(strip=True))
        current_page_value = pagination.find('li', class_='product-pagination__item active').get_text(strip=True)
        if int(current_page_value) != int(max_pages):
            get_products(url, next_page_ref)
    return results


time = datetime.now()
with open('atb.csv', 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ['ref', 'name', 'price', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for category in get_categories():
        print(f"Processing: {category}")
        writer.writerows(get_products(category))

print(f"All completed!\nElapsed time: {datetime.now() - time}")