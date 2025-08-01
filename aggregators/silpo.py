import csv
from datetime import datetime

import requests

from aggregators.base import GroceriesAggregator


class SilpoAggregator(GroceriesAggregator):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'utf-8',
        'Host': 'sf-ecom-api.silpo.ua',
        'Origin': 'https://silpo.ua',
        'Referer': 'https://silpo.ua/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Dest': 'empty',
        'Sec-GPC': '1',
        'TE': 'trailers',
        'Accept-Language': 'en-GB,en;q=0.5',
        }

    csv_schema = ['category', 'name', 'price', 'ref', 'shop']

    def get_categories(self):
        categories_url = "https://sf-ecom-api.silpo.ua/v1/branches/00000000-0000-0000-0000-000000000000/categories/tree"
        category_details_url = 'https://sf-ecom-api.silpo.ua/v1/uk/branches/00000000-0000-0000-0000-000000000000/categories/'


        params = {
            'deliveryType': 'DeliveryHome',
            'depth': '1',
        }

        response = requests.get(categories_url, headers=self.headers, params=params)
        return [
            (
                x['slug'],
                requests.get(category_details_url + x['slug'], headers=self.headers).json()['title'],
            ) for x in response.json()['items']
        ]


    def get_products(self, slugs, query_size=100, offset=0):
        url = "https://sf-ecom-api.silpo.ua/v1/uk/branches/00000000-0000-0000-0000-000000000000/products"
        category_slug, category_title = slugs

        results = []
        while True:
            params = {
                'deliveryType': 'DeliveryHome',
                'category': category_slug,
                'includeChildCategories': True,
                'sortBy': 'popularity',
                'sortDirection': 'desc',
                'inStock': 'false',
                'limit': query_size,
                'offset': offset,
            }
            response = requests.get(url, headers=self.headers, params=params).json()
            total_records = response['total']
            print(f'[{self.__class__.__name__}] current offset: {offset}')
            if offset > total_records:
                print(f'[{self.__class__.__name__}] All items collected!')
                break
            for item in response['items']:
                results.append(
                    {
                        'name': item['title'],
                        'ref': 'https://silpo.ua/product/' + item['sectionSlug'],
                        'price': format(item['displayPrice'], '.2f') + ' грн/'+ item['displayRatio'],
                        'category': category_title,
                        'shop': 'silpo',
                }
                )
            offset += query_size

        return results
