import scrapy
from itemloaders.processors import Compose, TakeFirst


def process_price(value):
    if not value:
        return
    return int("".join(value[0].split(" ")))


def process_name(value):
    # if not value:
    #     return

    print(value)
    return value.strip()


class LeroyMerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor=Compose(process_name), output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=Compose(process_price), output_processor=TakeFirst()
    )
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
