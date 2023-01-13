import scrapy
from scrapy.http import HtmlResponse

from vacancy_scrap.items import VacancyScrapItem


class SuperjobSpider(scrapy.Spider):
    name = "superjob"
    allowed_domains = ["superjob.ru"]
    start_urls = ["https://russia.superjob.ru/vacancy/search/?keywords=Python"]

    def parse(self, response: HtmlResponse):
        vacancies = response.xpath(
            "//div[contains(@class, 'f-test-vacancy-item')]/div/div[1]//a/@href"
        ).extract()
        for vacancy in vacancies:
            yield response.follow(vacancy, self.item_parse)

        next_page = response.xpath(
            "//a[contains(@class, 'f-test-button-dalshe')]/@href"
        ).extract_first()

        if next_page:
            yield response.follow("https://russia.superjob.ru" + next_page, self.parse)

    def item_parse(self, response: HtmlResponse):
        name = response.css("h1::text").extract_first()
        salary = response.xpath("//h1/following::span[1]/span/text()").extract()
        yield VacancyScrapItem(link=response.url, name=name, salary=salary)
