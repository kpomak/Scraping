import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst


def process_price(value):
    if not value:
        return
    return int("".join(value.split(" ")))


def process_name(value):
    if not value:
        return
    return value.strip()


def process_specs(value):
    print(value, "!!!!!!")
    return value


class LeroyMerlinItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor=MapCompose(process_name), output_processor=Join()
    )
    price = scrapy.Field(
        input_processor=MapCompose(process_price), output_processor=TakeFirst()
    )
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    # params = scrapy.Field(input_processor=MapCompose(process_specs), output_processor=Join())
