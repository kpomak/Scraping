import scrapy


class VacancyScrapItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
    salary_from = scrapy.Field()
    salary_upto = scrapy.Field()
    currency = scrapy.Field()
