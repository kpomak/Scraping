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
        if item["salary"]:
            self.get_salary(item)
        del item["salary"]
        collection.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)
        return item

    def get_id(self, link):
        id = re.search(r"\d+", link)[0]
        return id

    def get_salary(self, item):
        salary_parser = {
            "superjob.ru": self.sj_salary,
            "hh.ru": self.hh_salary,
        }
        money = item["salary"]
        length = len(money)
        if length <= 2:
            return
        money = self.prettify(item, money)
        salary_parser[item["source"]](item, money)

    def hh_salary(self, item, money):
        item["currency"] = money[-1]
        if len(money) == 6:
            item["salary_from"] = money[1]
            item["salary_upto"] = money[3]
        elif "от" in money:
            item["salary_from"] = money[1]
        else:
            item["salary_upto"] = money[1]

    def sj_salary(self, item, money):
        if len(money) == 5:
            item["salary_from"] = money[0]
            item["salary_upto"] = money[1]
            item["currency"] = money[3]
        elif "от" in money:
            item["salary_from"] = money[2]
        elif "до" in money:
            item["salary_from"] = money[2]
        else:
            item["salary_upto"] = money[0]
            item["currency"] = money[2]

    def prettify(self, item, money):
        for idx, coin in enumerate(money):
            if coin[0].isdigit():
                coin_value = "".join(coin.split())
                try:
                    item["salary"][idx] = int(coin_value)
                except ValueError:
                    item["currency"] = coin_value[-1]
                    item["salary"][idx] = int(coin_value[:-1])
        return money
