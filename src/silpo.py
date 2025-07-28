import csv
from datetime import datetime

import requests

headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
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

def get_categories():
    url = "https://sf-ecom-api.silpo.ua/v1/branches/00000000-0000-0000-0000-000000000000/categories/tree"
    category_details_url = 'https://sf-ecom-api.silpo.ua/v1/uk/branches/00000000-0000-0000-0000-000000000000/categories/'


    params = {
        'deliveryType': 'DeliveryHome',
        'depth': '1',
    }

    response = requests.get(url, headers=headers, params=params)
    return [
        (
            x['slug'],
            requests.get(category_details_url + x['slug'], headers=headers).json()['title'],
        ) for x in response.json()['items']
    ]


def get_products(slugs, query_size=100, offset=0):
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
        response = requests.get(url, headers=headers, params=params).json()
        total_records = response['total']
        print(f'current offset: {offset}')
        if offset > total_records:
            break
        for item in response['items']:
            results.append(
                {
                    'name': item['title'],
                    'ref': 'https://silpo.ua/product/' + item['sectionSlug'],
                    'price': format(item['displayPrice'], '.2f') + ' грн/'+ item['displayRatio'],
                    'category': category_title,
            }
            )
        offset += query_size

    return results

time = datetime.now()
with open('silpo.csv', 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ['ref', 'name', 'price', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    categories = get_categories()
    for category in categories:
        print(f"Processing: {category}")
        writer.writerows(get_products(category))

print(f"All completed!\nElapsed time: {datetime.now() - time}")