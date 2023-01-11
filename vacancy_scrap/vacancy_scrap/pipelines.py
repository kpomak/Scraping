from pymongo import MongoClient
import os
from dotenv import load_dotenv


class VacancyScrapPipeline:
    def __init__(self):
        load_dotenv()
        client = MongoClient(os.environ.get('MONGO_URI'))
        self.db = client.jobs

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.update_one({'_id':item['_id']})
        return item
