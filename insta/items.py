import scrapy


class InstaItem(scrapy.Item):
    _id = scrapy.Field()
    username = scrapy.Field()
    full_name = scrapy.Field()
    avatar = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
