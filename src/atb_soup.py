from urllib import request
from bs4 import BeautifulSoup

from src.base import GroceriesAggregator


class AtbAggregator(GroceriesAggregator):
    base_url = 'https://www.atbmarket.com'
    csv_schema = ['category', 'name', 'price', 'ref', 'shop']
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
    results = []

    def get_categories(self):

        response = request.Request(self.base_url, headers=self.headers)
        soup = BeautifulSoup(request.urlopen(response).read(), 'lxml')
        menu = soup.find('ul', class_='category-menu')
        menu_items = menu.find_all('li', class_='category-menu__item')

        return [self.base_url + x.find('a').get('href') for x in menu_items]

    def get_products(self, url, page=None):

        request_url = f'{url}?page={page}' if page else url
        print(f'getting products from: {request_url}')
        response = request.Request(request_url, headers=self.headers)

        soup = BeautifulSoup(request.urlopen(response).read(), 'lxml')
        catalog = soup.find('div', class_='catalog-list')
        catalog_items = catalog.find_all("article", class_='catalog-item')

        for item in catalog_items:
            self.results.append({
                'category': soup.find('h1', class_='page-title').get_text(strip=True),
                'name': item.find('div', class_='catalog-item__title').find('a').get_text(strip=True),
                'price': item.find('data', class_='product-price__top').get('value') +
                         ' ' +
                         item.find('abbr', class_='product-price__currency-abbr').get_text(strip=True),
                'ref': response.full_url + item.find('div', class_='catalog-item__title').find('a').get('href'),
                'shop': 'atb'
            }
            )
        pagination = soup.find('ul', class_='product-pagination__list')
        if pagination:
            max_pages = pagination.find_all('li', class_='product-pagination__item')[-2].get_text(strip=True)
            next_page_num = (pagination.find('li', class_='product-pagination__item active')
                             .find_next('li', class_='product-pagination__item')
                             .get_text(strip=True))
            current_page_value = pagination.find('li', class_='product-pagination__item active').get_text(strip=True)
            if int(current_page_value) != int(max_pages):
                self.get_products(url, next_page_num)
        return self.results

    def get_products_bulk(self):
        bulk_results = []
        categories = self.get_categories()
        for category in categories:
           bulk_results += self.get_products(category)

        return bulk_results