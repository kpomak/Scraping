# from itemadapter import ItemAdapter
from pymongo import MongoClient


class VacancyScrapPipeline:
    def __init__(self):
        client = MongoClient(mongo_uri)
        self.db = client.jobs

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        return item
