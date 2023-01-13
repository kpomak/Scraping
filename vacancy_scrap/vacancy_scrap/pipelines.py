import re

from pymongo import MongoClient


class VacancyScrapPipeline:
    def __init__(self):
        client = MongoClient("mongodb://root:pass@localhost:27017/")
        self.db = client.jobs

    def process_item(self, item, spider):
        collection = self.db.vacancies
        item["_id"] = self.get_id(item["link"]) + spider.name[:2]
        item["source"] = spider.allowed_domains[0]
        self.get_salary(item)
        # del item["salary"]
        collection.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)
        return item

    def get_id(self, link):
        id = re.search(r"\d+", link)[0]
        return id

    def get_salary(self, item):
        # money = self.prettify(item["salary"])
        money = item["salary"]
        length = len(money)
        if length <= 2:
            return
        item["currency"] = money[-1]
        if length == 6:
            item["salary_from"] = money[1]
            item["salary_upto"] = money[3]
        elif "от" in money:
            item["salary_from"] = money[1]
        else:
            item["salary_upto"] = money[1]

    def prettify(self, money):
        for idx, coin in enumerate(money):
            if coin[0].isdigit():
                money[idx] = int("".join(money.split()))
        return money
