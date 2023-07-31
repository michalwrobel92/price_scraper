from django.apps import AppConfig


class PriceScrapperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'price_scrapper'

    def ready(self):
        from .scrapy.spiders.selgros24spider import Selgros24spiderSpider
        from scrapy.crawler import CrawlerProcess

        process = CrawlerProcess()
        process.crawl(Selgros24spiderSpider)
        process.start()
