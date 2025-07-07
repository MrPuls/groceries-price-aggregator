import scrapy

class SilpoSpider(scrapy.Spider):
    def parse(self, response):
        for item in response.css("div.products-list__item"):
            yield {
                "name": item.css('div.product-card__title::text').get(),
                "price": item.css('div.product-card-price__displayPrice::text').get(),
            }
        current_page = response.url.replace('https://silpo.ua', '')
        # links = response.css("div.pagination__items a::attr(href)").getall()
        # try:
        #     next_page = links[links.index(current_page) + 1]
        # except IndexError:
        #     next_page = None

        # TODO: As an optimization, we can skip the products which are unavailable or out of stock

        # TODO: Perhaps this process can be parallelized too? Something like
        #  "get amount of pages and crawl 50 with each iteration"

        # TODO: This one is more stable but ignores last page
        next_page = response.css('.pagination-item.pagination-item--next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

class FruitsAndVegetablesSpider(SilpoSpider):
    name = "vegetables_and_fruits"
    start_urls = ["https://silpo.ua/category/frukty-ovochi-4788"]
    custom_settings = {
        'FEEDS': {
            'results/vegetables_and_fruits.csv': {'format': 'csv'},
        }
    }

class MeatSpider(SilpoSpider):
    name = "meat"
    start_urls = ["https://silpo.ua/category/m-iaso-4411"]
    custom_settings = {
        'FEEDS': {
            'results/meat.csv': {'format': 'csv'},
        }
    }

class SausagesAndDelicaciesSpider(SilpoSpider):
    name = "sausages_and_delicacies"
    start_urls = ["https://silpo.ua/category/kovbasni-vyroby-i-m-iasni-delikatesy-4731"]
    custom_settings = {
        'FEEDS': {
            'results/sausages_and_delicacies.csv': {'format': 'csv'},
        }
    }

class CheeseSpider(SilpoSpider):
    name = "cheese"
    start_urls = ["https://silpo.ua/category/syry-1468"]
    custom_settings = {
        'FEEDS': {
            'results/cheese.csv': {'format': 'csv'},
        }
    }

class BreadAndBakerySpider(SilpoSpider):
    name = "bread_and_bakery"
    start_urls = ["https://silpo.ua/category/khlib-ta-vypichka-5121"]
    custom_settings = {
        'FEEDS': {
            'results/bread_and_bakery.csv': {'format': 'csv'},
        }
    }

class TakeoutSpider(SilpoSpider):
    name = "takeout"
    start_urls = ["https://silpo.ua/category/gotovi-stravy-i-kulinariia-4761"]
    custom_settings = {
        'FEEDS': {
            'results/takeout.csv': {'format': 'csv'},
        }
    }

class MilkAndEggsSpider(SilpoSpider):
    name = "milk_and_eggs"
    start_urls = ["https://silpo.ua/category/molochni-produkty-ta-iaitsia-234"]
    custom_settings = {
        'FEEDS': {
            'results/milk_and_eggs.csv': {'format': 'csv'},
        }
    }

class InternalProductsSpider(SilpoSpider):
    name = "internal_products"
    start_urls = ["https://silpo.ua/category/vlasni-marky-5202"]
    custom_settings = {
        'FEEDS': {
            'results/internal_products.csv': {'format': 'csv'},
        }
    }

class TraditionStandSpider(SilpoSpider):
    name = "tradition_stand"
    start_urls = ["https://silpo.ua/category/lavka-tradytsii-4487"]
    custom_settings = {
        'FEEDS': {
            'results/tradition_stand.csv': {'format': 'csv'},
        }
    }
# TODO: Broken
class HealthyFoodsSpider(SilpoSpider):
    name = "healthy_foods"
    start_urls = ["https://silpo.ua/category/zdorove-kharchuvannia-4864"]
    custom_settings = {
        'FEEDS': {
            'results/healthy_foods.csv': {'format': 'csv'},
        }
    }

class GroceriesSpider(SilpoSpider):
    name = "groceries"
    start_urls = ["https://silpo.ua/category/bakaliia-i-konservy-4870"]
    custom_settings = {
        'FEEDS': {
            'results/groceries.csv': {'format': 'csv'},
        }
    }

class SousesAndSpicesSpider(SilpoSpider):
    name = "souses_and_spices"
    start_urls = ["https://silpo.ua/category/sousy-i-spetsii-4938"]
    custom_settings = {
        'FEEDS': {
            'results/souses_and_spices.csv': {'format': 'csv'},
        }
    }

class SweetsSpider(SilpoSpider):
    name = "sweets"
    start_urls = ["https://silpo.ua/category/solodoshchi-498"]
    custom_settings = {
        'FEEDS': {
            'results/sweets.csv': {'format': 'csv'},
        }
    }

class SnacksSpider(SilpoSpider):
    name = "snacks"
    start_urls = ["https://silpo.ua/category/sneky-ta-chypsy-5016"]
    custom_settings = {
        'FEEDS': {
            'results/snacks.csv': {'format': 'csv'},
        }
    }

class CoffeeAndTeaSpider(SilpoSpider):
    name = "coffee_and_tea"
    start_urls = ["https://silpo.ua/category/kava-chai-359"]
    custom_settings = {
        'FEEDS': {
            'results/coffee_and_tea.csv': {'format': 'csv'},
        }
    }

class DrinksSpider(SilpoSpider):
    name = "drinks"
    start_urls = ["https://silpo.ua/category/napoi-52"]
    custom_settings = {
        'FEEDS': {
            'results/drinks.csv': {'format': 'csv'},
        }
    }

class FrozenSpider(SilpoSpider):
    name = "frozen"
    start_urls = ["https://silpo.ua/category/zamorozhena-produktsiia-264"]
    custom_settings = {
        'FEEDS': {
            'results/frozen.csv': {'format': 'csv'},
        }
    }

class AlcoholSpider(SilpoSpider):
    name = "alcohol"
    start_urls = ["https://silpo.ua/category/alkogol-22"]
    custom_settings = {
        'FEEDS': {
            'results/alcohol.csv': {'format': 'csv'},
        }
    }

class CigarettesSpider(SilpoSpider):
    name = "cigarettes"
    start_urls = ["https://silpo.ua/category/sygarety-stiky-zhuiky-4384"]
    custom_settings = {
        'FEEDS': {
            'results/cigarettes.csv': {'format': 'csv'},
        }
    }

class FlowersSpider(SilpoSpider):
    name = "flowers"
    start_urls = ["https://silpo.ua/category/kvity-tovary-dlia-sadu-ta-gorodu-476"]
    custom_settings = {
        'FEEDS': {
            'results/flowers.csv': {'format': 'csv'},
        }
    }

class HomeProductsSpider(SilpoSpider):
    name = "home_products"
    start_urls = ["https://silpo.ua/category/dlia-domu-567"]
    custom_settings = {
        'FEEDS': {
            'results/home_products.csv': {'format': 'csv'},
        }
    }

class HygieneSpider(SilpoSpider):
    name = "hygiene"
    start_urls = ["https://silpo.ua/category/gigiiena-ta-krasa-4519"]
    custom_settings = {
        'FEEDS': {
            'results/hygiene.csv': {'format': 'csv'},
        }
    }

class KidsProductsSpider(SilpoSpider):
    name = "kids_products"
    start_urls = ["https://silpo.ua/category/dytiachi-tovary-449"]
    custom_settings = {
        'FEEDS': {
            'results/kids_products.csv': {'format': 'csv'},
        }
    }

class PetProductsSpider(SilpoSpider):
    name = "pet_products"
    start_urls = ["https://silpo.ua/category/dlia-tvaryn-653"]
    custom_settings = {
        'FEEDS': {
            'results/pet_products.csv': {'format': 'csv'},
        }
    }