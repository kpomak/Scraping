import os

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class InstaPipeline:
    def __init__(self):
        mongo_uri = os.getenv("MONGODB_URI")
        client = MongoClient(mongo_uri)
        db = client.social
        self.collection = db.instagram

    def process_item(self, item, spider):
        record_user = self.collection.find_one({"_id": item["_id"]})
        if not record_user:
            self.collection.insert_one(item)
        elif item.get("followers"):
            self.collection.update_one(
                {"_id": item["_id"]}, {"$push": {"followers": item["followers"].pop()}}
            )
        else:
            self.collection.update_one(
                {"_id": item["_id"]}, {"$push": {"following": item["following"].pop()}}
            )
        return item


class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        avatar_url = item.get("avatar")
        if avatar_url:
            try:
                yield scrapy.Request(avatar_url)
            except Exception as error:
                print(error)

    def item_completed(self, results, item, info):
        if results:
            item["avatar"] = [result["path"] for ok, result in results if ok].pop()
        return item
