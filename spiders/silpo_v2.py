import logging
from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class SilpoSpider(scrapy.Spider):
    name = "silpo_v2"
    base_url = "https://silpo.ua"
    start_urls = [
        "https://silpo.ua/category/frukty-ovochi-4788",
        "https://silpo.ua/category/m-iaso-4411",
        "https://silpo.ua/category/kovbasni-vyroby-i-m-iasni-delikatesy-4731",
        "https://silpo.ua/category/syry-1468",
        "https://silpo.ua/category/khlib-ta-vypichka-5121",
        "https://silpo.ua/category/gotovi-stravy-i-kulinariia-4761",
        "https://silpo.ua/category/molochni-produkty-ta-iaitsia-234",
        "https://silpo.ua/category/vlasni-marky-5202",
        "https://silpo.ua/category/lavka-tradytsii-4487",
        "https://silpo.ua/category/zdorove-kharchuvannia-4864",
        "https://silpo.ua/category/bakaliia-i-konservy-4870",
        "https://silpo.ua/category/sousy-i-spetsii-4938",
        "https://silpo.ua/category/solodoshchi-498",
        "https://silpo.ua/category/sneky-ta-chypsy-5016",
        "https://silpo.ua/category/kava-chai-359",
        "https://silpo.ua/category/napoi-52",
        "https://silpo.ua/category/zamorozhena-produktsiia-264",
        "https://silpo.ua/category/alkogol-22",
        "https://silpo.ua/category/sygarety-stiky-zhuiky-4384",
        "https://silpo.ua/category/kvity-tovary-dlia-sadu-ta-gorodu-476",
        "https://silpo.ua/category/gigiiena-ta-krasa-4519",
        "https://silpo.ua/category/dytiachi-tovary-449",
        "https://silpo.ua/category/dlia-tvaryn-653",
        "https://silpo.ua/category/dlia-domu-567",
        "https://silpo.ua/category/ryba-4430",
        # "https://silpo.ua/category/spetsialni-propozytsii-5189" # not sure if needed yet
    ]
    def parse(self, response):
        for item in response.css("div.products-list__item"):
            yield {
                "name": item.css('div.product-card__title::text').get(),
                "price": item.css('div.product-card-price__displayPrice::text').get(),
                "category": response.css('h1.catalog__products-title::text').get(),
                "page": response.css('.pagination-item.pagination-item--current::text').get(),
                "ref": self.base_url + item.css('a.product-card::attr(href)').get()
            }
        # TODO: Ignores the last page. Need a fix
        next_page = response.css('.pagination-item.pagination-item--next-page::attr(href)').get()
        if not next_page:
            next_page = response.css('.pagination-item.pagination-item:nth-last-child(2)::attr(href)').get()

        if next_page[-2:] != response.url[-2:]:
            yield response.follow(next_page, callback=self.parse)

if __name__ == '__main__':
    time = datetime.now()
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(SilpoSpider)
    process.start()
    logging.info(f"All spiders completed!\nElapsed time: {datetime.now() - time}")