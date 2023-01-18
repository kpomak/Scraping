import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def process_price(value):
    if not value:
        return
    return int("".join(value.split(" ")))


def process_striptease(value):
    if not value:
        return
    return value.strip()


class LeroyMerlinItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(
        input_processor=MapCompose(process_striptease), output_processor=Join()
    )
    price = scrapy.Field(
        input_processor=MapCompose(process_price), output_processor=TakeFirst()
    )
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field()
    param_label = scrapy.Field(input_processor=MapCompose(process_striptease))
    param_value = scrapy.Field(input_processor=MapCompose(process_striptease))
