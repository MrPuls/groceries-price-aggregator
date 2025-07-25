import requests

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

category_url = 'https://stores-api.zakaz.ua/stores/48215614/categories/'
products_url = 'https://stores-api.zakaz.ua/stores/48215614/categories/dairy-and-eggs-metro/products?page=1'
categories = []

params = {
    'only_parents': 'false',
}

response = requests.get(category_url, headers=headers, params=params)

for item in response.json():
    categories.append((item['id'], item['title']))

