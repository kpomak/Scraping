import scrapy
from itemloaders.processors import TakeFirst, Compose


def process_price(value):
    if not value:
        return
    return {
        "money": value,
        "currency": value,
    }


class LeroyMerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(
        input_processor=Compose(process_price), output_processor=TakeFirst()
    )
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
