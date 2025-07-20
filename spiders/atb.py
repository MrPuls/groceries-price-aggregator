import scrapy
from scrapy import Request


class AtbSpider(scrapy.Spider):
    name = "atb"
    urls = [
        'https://www.atbmarket.com/catalog/287-ovochi-ta-frukti',
        'https://www.atbmarket.com/catalog/285-bakaliya',
        'https://www.atbmarket.com/catalog/molocni-produkti-ta-ajca',
        'https://www.atbmarket.com/catalog/292-alkogol-i-tyutyun',
        'https://www.atbmarket.com/catalog/294-napoi-bezalkogol-ni',
        'https://www.atbmarket.com/catalog/siri',
        'https://www.atbmarket.com/catalog/maso',
        'https://www.atbmarket.com/catalog/299-konditers-ki-virobi',
        'https://www.atbmarket.com/catalog/353-riba-i-moreprodukti',
        'https://www.atbmarket.com/catalog/325-khlibobulochni-virobi',
        'https://www.atbmarket.com/catalog/322-zamorozheni-produkti',
        'https://www.atbmarket.com/catalog/kava-caj',
        'https://www.atbmarket.com/catalog/cipsi-sneki',
        'https://www.atbmarket.com/catalog/360-kovbasa-i-m-yasni-delikatesi',
        'https://www.atbmarket.com/catalog/339-dityache-kharchuvannya',
        'https://www.atbmarket.com/catalog/415-yapons-ka-kukhnya',
        'https://www.atbmarket.com/catalog/373-tovari-dlya-ditey',
        'https://www.atbmarket.com/catalog/308-pobutova-khimiya-ta-neprodovol-chi-tovari',
        'https://www.atbmarket.com/catalog/290-gigiena-i-kosmetika',
        'https://www.atbmarket.com/catalog/358-tovari-dlya-domu',
        'https://www.atbmarket.com/catalog/436-tovari-dlya-tvarin',
        'https://www.atbmarket.com/catalog/479-tyutyunovi-virobi',
        'https://www.atbmarket.com/catalog/389-kantselyars-ki-tovari'
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'
    }


    async def start(self):
        for url in self.urls:
            yield Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for item in response.css("article.catalog-item"):
            # from scrapy.shell import inspect_response
            #
            # inspect_response(response, self)
            yield {
                'title': response.css("h1.page-title::text").get(),
                'name': item.css('div.catalog-item__title a::text').get(),
                'price': item.css('data.product-price__top::attr(value)').get() +
                         ' ' +
                         item.css('abbr.product-price__currency-abbr::text').get() +
                         item.css('span.product-price__unit::text').get(),
                'ref': response.url + item.css('div.catalog-item__title a::attr(href)').get(),
            }

        max_pages = response.css("li.product-pagination__item:nth-last-child(2) a::text").get()
        next_page_ref = response.css('li.product-pagination__item.active + li a::attr(href)').get()
        current_page_value = response.css('li.product-pagination__item.active a::text').get()
        if current_page_value != max_pages:
            yield response.follow(next_page_ref, callback=self.parse, headers=self.headers)