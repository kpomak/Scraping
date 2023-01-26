import re

import scrapy
from scrapy.http import HtmlResponse

from insta import settings


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    login = settings.LOGIN
    password = settings.PASSWORD
    accounts = settings.USERS_LIST
    api_url = "https://www.instagram.com/graphql/query/?"

    def parse(self, response: HtmlResponse):
        token = self.get_csrf(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.parse_user,
            headers={
                "X-CSRFToken": token,
            },
            formdata={
                "enc_password": self.password,
                "username": self.login,
                "queryParams": {},
                "optIntoOneTap": "false",
                "trustedDeviceRecords": {},
            },
        )

    def parse_user(self, response: HtmlResponse):
        json_data = response.json()
        if json_data.get("authenticated"):
            _id = json_data.get("userId")
            print("well done")

    def get_csrf(self, text):
        token = re.search('csrf_token\\\\":\\\\"\w+', text).group()
        return token.split('"').pop()
