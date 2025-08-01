import json

import requests

from aggregators.base import GroceriesAggregator


class VarusAggregator(GroceriesAggregator):

    products_url = "https://varus.ua/api/catalog/vue_storefront_catalog_2/product_v2/_search"
    categories_url = "https://varus.ua/api/catalog/vue_storefront_catalog_2/banner/_search"
    csv_schema = ['category', 'name', 'price', 'ref', 'shop']
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"
    }

    def get_categories(self):
        categories_request_data = {
            "_availableFilters": [],
            "_appliedFilters": [
                {"attribute": "datetime_from", "value": {"lt": "now"}, "scope": "default"},
                {"attribute": "datetime_to", "value": {"gt": "now-1d"}, "scope": "default"},
                {"attribute": "status", "value": {"eq": "1"}, "scope": "default"},
                {"attribute": "position", "value": {"eq": "3"}, "scope": "default"}
            ],
            "_appliedSort": [],
            "_searchText": ""
        }
        categories_params = {
            "_source_exclude": "tms,tsk,sgn,paths,created_time,update_time",
            "from": 0,
            "request": json.dumps(categories_request_data),
            "request_format": "search-query",
            "response_format": "compact",
            "size": 50,
            "sort": ""
        }
        response = requests.get(self.categories_url, params=categories_params, headers=self.headers)
        categories_results = []

        for item in response.json()['hits']:
            categories_results.append(([item["link"]], item['category_ids']))
        return categories_results

    def get_products(self, category_ids: tuple, query_size=100, offset=0):
        # TODO: Perhaps remove unused sources from products_params
        category, category_ids = category_ids
        print(f'[{self.__class__.__name__}] Got category: {category}')
        products_request_data = {
            "_availableFilters": [
                {"field": "pim_brand_id", "scope": "catalog", "options": {}},
                {"field": "countrymanufacturerforsite", "scope": "catalog", "options": {}},
                {"field": "promotion_banner_ids", "scope": "catalog", "options": {}},
                {"field": "price", "scope": "catalog", "options": {"shop_id": 3, "version": "2"}},
                {"field": "has_promotion_in_stores", "scope": "catalog", "options": {"size": 10000}},
                {"field": "markdown_id", "scope": "catalog", "options": {}}
            ],
            "_appliedFilters": [
                {"attribute": "visibility", "value": {"in": [2, 4]}, "scope": "default"},
                {"attribute": "status", "value": {"in": [0, 1]}, "scope": "default"},
                {
                    "attribute": "category_ids", "value": {
                    "in": category_ids
                },
                    "scope": "default"},
                {"attribute": "markdown_id", "value": {"or": None}, "scope": "default"},
                {"attribute": "sqpp_data_3.in_stock", "value": {"or": True}, "scope": "default"},
                {"attribute": "markdown_id", "value": {"nin": None}, "scope": "default"}
            ],
            "_appliedSort": [
                {
                    "field": "_script",
                    "options": {
                        "type": "number",
                        "order": "desc",
                        "script": {
                            "lang": "painless",
                            "source":
                                "\nint score = 0;\n\nscore = doc['sqpp_data_region_default.availability.shipping'].value ?"
                                " 2 : score;\nscore = doc['sqpp_data_region_default.availability.other_regions'].value ?"
                                " 2 : score;\nscore = doc['sqpp_data_region_default.availability.pickup'].value ?"
                                " 2 : score;\nscore = doc['sqpp_data_region_default.availability.other_market'].value ?"
                                " 2 : score;\nscore = doc['sqpp_data_region_default.availability.delivery'].value ?"
                                " 4: score;\n\nscore += doc['sqpp_data_region_default.in_stock'].value ? 1 : 0;"
                                "\n\nif (doc.containsKey('markdown_id') && !doc['markdown_id'].empty && score > 2) "
                                "{\n score = 3;\n}\n\nreturn score;\n"
                        }
                    }
                },
                {"field": "category_position_2", "options": {"order": "desc"}},
                {"field": "sqpp_score", "options": {"order": "desc"}}
            ],
            "_searchText": ""
        }
        results = []
        while True:
            products_params = {
                "_source_exclude": "",
                "_source_include": "brand_data.name,description,category,category_ids,stock.is_in_stock,forNewPost,stock.qty,"
                                   "stock.max,stock.manage_stock,stock.is_qty_decimal,sku,id,name,image,regular_price,"
                                   "special_price_discount,special_price_to_date,slug,url_key,url_path,product_label,"
                                   "type_id,volume,weight,wghweigh,packingtype,is_new,is_18_plus,news_from_date,news_to_date,"
                                   "varus_perfect,productquantityunit,productquantityunitstep,productminsalablequantity,"
                                   "productquantitysteprecommended,markdown_id,markdown_title,markdown_discount,"
                                   "markdown_description,online_promotion_in_stores,boardProduct,fv_image_timestamp,"
                                   "sqpp_data_region_default",
                "from": offset,
                "request": json.dumps(products_request_data),
                "request_format": "search-query",
                "response_format": "compact",
                "shop_id": 3,
                "size": query_size,
                "sort": ""
            }
            response = requests.get(self.products_url, params=products_params, headers=self.headers)
            products = response.json()['hits']
            total_records = response.json()['total']['value']
            print(f"[{self.__class__.__name__}] Current from value is: {offset}")
            if offset > total_records:
                break
            for item in products:
                results.append({
                    'ref': item['url_key'],
                    'name': item['name'],
                    'price': format(item['sqpp_data_region_default']['price'], '.2f') + ' грн',
                    'category': [x['name'] for x in item['category'] if x['category_id'] in category_ids],
                    'shop': 'varus'
                })
            offset += query_size
        return results