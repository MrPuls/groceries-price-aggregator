import csv
from datetime import datetime

import requests

from src.base import GroceriesAggregator


class AtbAggregator(GroceriesAggregator):
    headers = {
        'Host': 'stores-api.zakaz.ua',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
        'Accept': '*/*',
        'Accept-Language': 'uk',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://metro.zakaz.ua/uk/',
        'Content-Type': 'application/json',
        'x-chain': 'metro',
        'X-Delivery-Type': 'plan',
        'x-version': '65',
        'Origin': 'https://metro.zakaz.ua',
        'Sec-GPC': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'content-language': 'uk',
    }
    category_params = {
        'only_parents': 'false',
    }
    category_url = 'https://stores-api.zakaz.ua/stores/48215614/categories/'
    csv_schema = ['category', 'name', 'price', 'ref', 'shop']

    def get_categories(self):
        category_response = requests.get(self.category_url, headers=self.headers, params=self.category_params)
        return [(x['id'], x['title']) for x in category_response.json()]

    def get_products(self, category: tuple):
        products = []
        products_url = f'https://stores-api.zakaz.ua/stores/48215614/categories/{category[0]}/products'
        product_params_page = 1
        while True:
            product_params = {
                'page': f'{product_params_page}'
            }
            products_response = requests.get(products_url, headers=self.headers, params=product_params)
            products_response_results = products_response.json()['results']

            if not products_response_results:
                break

            for product in products_response_results:
                products.append({
                    'name': product['title'],
                    'price': format(product['price'] / 100, '.2f') + ' грн',
                    'ref': product['web_url'],
                    'category': category[1],
                    'shop': 'metro',
                })

            product_params_page += 1

        if len(products) == products_response.json()['count']:
            print(f'All items collected!')
        return products

    def get_products_bulk(self):
        bulk_results = []
        for category in self.get_categories():
            products = self.get_products(category)
            bulk_results += products
        return bulk_results
