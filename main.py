# import multiprocessing
# from datetime import datetime
# from multiprocessing import Pool
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
#
# import spiders.silpo_spiders as spiders
#
# spider_list = [
#     spiders.FruitsAndVegetablesSpider,
#     spiders.MeatSpider,
#     spiders.SausagesAndDelicaciesSpider,
#     spiders.CheeseSpider,
#     spiders.BreadAndBakerySpider,
#     spiders.TakeoutSpider,
#     spiders.MilkAndEggsSpider,
#     spiders.InternalProductsSpider,
#     spiders.TraditionStandSpider,
#     spiders.HealthyFoodsSpider,
#     spiders.GroceriesSpider,
#     spiders.SousesAndSpicesSpider,
#     spiders.SweetsSpider,
#     spiders.SnacksSpider,
#     spiders.CoffeeAndTeaSpider,
#     spiders.DrinksSpider,
#     spiders.FrozenSpider,
#     spiders.AlcoholSpider,
#     spiders.CigarettesSpider,
#     spiders.FlowersSpider,
#     spiders.HomeProductsSpider,
#     spiders.HygieneSpider,
#     spiders.KidsProductsSpider,
#     spiders.PetProductsSpider,
# ]
#
# def run_spider(spider):
#     settings = get_project_settings()
#     process = CrawlerProcess(settings)
#     process.crawl(spider)
#     process.start()
#
#
# if __name__ == '__main__':
#     # TODO: Either try and play more with the settings or try and separate spiders into groups and run a
#     #  CrawlerProcess group in a separate process. They might be slower, but perhaps more stable
#
#     time = datetime.now()
#     mp = []
#     for item in spider_list:
#         p = multiprocessing.Process(target=run_spider, args=(item,))
#         p.start()
#         mp.append(p)
#
#     for p in mp:
#         p.join()
#
#     print(f"All spiders completed!\nElapsed time: {datetime.now() - time}")