import os
import re

from dotenv import load_dotenv
from pymongo import MongoClient


class VacancyScrapPipeline:
    def __init__(self):
        load_dotenv()
        client = MongoClient(os.environ.get("MONGO_URI"))
        self.db = client.jobs

    def process_item(self, item, spider):
        collection = self.db.vacancies
        item["_id"] = self.get_id(item["link"]) + spider.name[:2]
        item["source"] = spider.allowed_domains[0]
        self.get_salary(item)
        del item["salary"]
        collection.update_one({"_id": item["_id"]}, {'$set': item}, upsert=True)
        return item

    def get_id(self, link):
        id = re.search(r'\d+', link)[0]
        return id

    def get_salary(self, item):
        money = item["salary"]
        length = len(money)
        if length <= 2:
            return
        item["currency"] = money[-1]
        if length == 6:
            item["salary_from"] = self.prettify(money[1])
            item["salary_upto"] = self.prettify(money[3])
        elif "от" in money:
            item["salary_from"] = self.prettify(money[1])
        else:
            item["salary_upto"] = self.prettify(money[1])

    def prettify(self, money):
        return int("".join(money.split()))



