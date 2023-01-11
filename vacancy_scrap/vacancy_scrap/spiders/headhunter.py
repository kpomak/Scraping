import scrapy
from scrapy.http import HtmlResponse
from vacancy_scrap import VacancyScrapItem


class HeadhunterSpider(scrapy.Spider):
    name = "headhunter"
    allowed_domains = ["hh.ru"]
    start_urls = [
        "https://spb.hh.ru/search/vacancy?area=2&text=django&from=suggest_post&items_on_page=20&hhtmFrom=vacancy_search_list"
    ]

    def parse(self, response: HtmlResponse):
        vacancies = response.xpath("//a[@class='serp-item__tittle']/@href").extract()
        for vacancy in vacancies:
            yield response.follow(vacancy, self.item_parse)

        next_page = response.xpath("//a[@data-qa='pager-next']").extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)

    def item_parse(self, response: HtmlResponse):
        name = response.css("h1::text").extract_first()
        print(1)
