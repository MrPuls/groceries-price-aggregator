import scrapy


class QuotesSpider(scrapy.Spider):
    name = "silpo"
    start_urls = ["https://silpo.ua/category/frukty-ovochi-4788"]

    def parse(self, response):
        for item in response.css("div.products-list__item"):
            yield {
                "name": item.css('div.product-card__title::text').get(),
                "price": item.css('div.product-card-price__displayPrice::text').get(),
            }
        current_page = response.url.replace('https://silpo.ua', '')
        links = response.css("div.pagination__items a::attr(href)").getall()
        next_page = links[links.index(current_page) + 1]

        if next_page:
            yield response.follow(next_page, callback=self.parse)