import scrapy


class MerlinSpider(scrapy.Spider):
    name = 'merlin'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def parse(self, response):
        pass
