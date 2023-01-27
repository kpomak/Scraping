import re
from copy import deepcopy

import scrapy
from scrapy.http import HtmlResponse

from insta import settings
from insta.items import InstaItem


class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = ["instagram.com"]
    start_urls = ["https://www.instagram.com/"]
    login_url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    account_url = "https://www.instagram.com/api/v1/users/web_profile_info/?username="
    login = settings.LOGIN
    password = settings.PASSWORD
    accounts = settings.USERS_LIST
    api_url = "https://www.instagram.com/api/v1/friendships/"

    def parse(self, response: HtmlResponse):
        """
        func requests main page and sends login form to authenticate spider
        """
        token = self.get_csrf(response.text)
        yield scrapy.FormRequest(
            self.login_url,
            method="POST",
            callback=self.parse_accounts,
            headers={
                "X-CSRFToken": token,
            },
            formdata={
                "enc_password": self.password,
                "username": self.login,
                "queryParams": "{}",
                "optIntoOneTap": "false",
                "trustedDeviceRecords": "{}",
            },
        )

    def parse_accounts(self, response: HtmlResponse):
        """
        func requests account info of users in USERS_LIST
        """
        login_confirm = response.json()
        if login_confirm.get("authenticated"):
            # id = login_confirm.get("userId")
            for user in self.accounts:
                yield response.follow(
                    f"{self.account_url}{user}",
                    callback=self.parse_user,
                    cb_kwargs={"username": user},
                )

    def parse_user(self, response: HtmlResponse, username):
        """
        func requests followers and following urls
        """
        id = self.get_user_id(response.text)

        followers_url = (
            f"{self.api_url}{id}/followers?count=12&search_surface=follow_list_page"
        )
        following_url = f"{self.api_url}{id}/following?count=12"

        yield response.follow(
            followers_url,
            callback=self.followers,
            cb_kwargs={
                "username": username,
                "id": id,
            },
        )

        yield response.follow(
            following_url,
            callback=self.following,
            cb_kwargs={
                "username": username,
                "id": id,
            },
        )

    def followers(self, response: HtmlResponse, username, id):
        """
        func scraps followers data
        """
        parsed_data = response.json()
        next = parsed_data.get("next_max_id")
        if next:
            followers_url = f"{self.api_url}{id}/followers?count=12&search_surface=follow_list_page&max_id={next}"
            yield response.follow(
                followers_url,
                callback=self.followers,
                cb_kwargs={
                    "username": username,
                    "id": id,
                },
            )
        users = parsed_data.get("users")
        for user in users:
            yield InstaItem(
                _id=user["pk"],
                username=user["username"],
                full_name=user["full_name"],
                avatar=user["profile_pic_url"],
                following=[id],
            )

    def following(self, response: HtmlResponse, username, id):
        """
        func parses following data
        """
        parsed_data = response.json()
        next = parsed_data.get("next_max_id")
        if next:
            following_url = f"{self.api_url}{id}/following?count=12&max_id={next}"
            yield response.follow(
                following_url,
                callback=self.following,
                cb_kwargs={
                    "username": username,
                    "id": id,
                },
            )
        users = parsed_data.get("users")
        for user in users:
            yield InstaItem(
                _id=user["pk"],
                username=user["username"],
                full_name=user["full_name"],
                avatar=user["profile_pic_url"],
                follower=[id],
            )

    def get_user_id(self, text):
        """
        func returns users id from response of profile-url request
        """
        id = re.search(r'("id":")(\d+)(","profile_pic_url)', text).group(2)
        return id

    def get_csrf(self, text):
        """
        func returns csrf-token from response of main page request
        """
        token = re.search('csrf_token\\\\":\\\\"\w+', text).group()
        return token.split('"').pop()
