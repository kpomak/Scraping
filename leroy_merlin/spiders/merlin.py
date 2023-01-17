import scrapy
from scrapy.http import HtmlResponse
from leroy_merlin.items import LeroyMerlinItem
from scrapy.loader import ItemLoader


class MerlinSpider(scrapy.Spider):
    name = "merlin"
    allowed_domains = ["castorama.ru"]
    # start_urls = ["https://www.castorama.ru/novogodnie-tovary/girlyandy/"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        search_string = kwargs.get('search')
        if search_string:
            self.start_urls = [f"https://www.castorama.ru/novogodnie-tovary/{search_string}/"]
        else:
            self.start_urls = ["https://www.castorama.ru/novogodnie-tovary/"]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "product-card__name")]/@href').extract()
        for link in links:
            yield response.follow(link, self.parse_item)

        next_page = response.xpath('//a[@class="next i-next"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyMerlinItem(), response=response)
        # loader.add_xpath('name', "//h1/text()")
        # loader.add_xpath('price', "//h3//text()")
        # loader.add_xpath('photos', "//div[@class='swiper-zoom-container']/img/@src | //div[@class='swiper-zoom-container']/img/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

    def parse_item(self, response: HtmlResponse):
        pass
