import scrapy
from scrapy.http import HtmlResponse

from insta import settings


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["http://instagram.com/"]
    login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    ogin = settings.LOGIN
    password = settings.PASSWORD
    accounts = settings.USERS_LIST
    api_url = "https://www.instagram.com/graphql/query/?"

    def parse(self, response: HtmlResponse):
        pass
