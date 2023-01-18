import hashlib

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class ParseLeroyMerlinPipeline:
    def __init__(self) -> None:
        client = MongoClient("mongodb://root:pass@localhost:27017")
        self.db = client.castorama

    def get_params(self, item):
        item["params"] = dict(zip(item["param_label"], item["param_value"]))

    def process_item(self, item, spider):
        collection = self.db.ligts
        if item["param_label"]:
            self.get_params(item)
        del item["param_label"]
        del item["param_value"]
        collection.update_one({"_id": item["_id"]}, {"$set": item}, upsert=True)
        return item


class PhotoLeroyMerlinPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item.get("photos"):
            for img in item.get("photos"):
                try:
                    yield scrapy.Request(
                        "https://www.castorama.ru" + img, meta={"name": item["name"]}
                    )
                except Exception as error:
                    print(error)

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1((request.url).encode("utf-8")).hexdigest()
        return f"{request.meta['name']}/{image_guid}.jpg"

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [result[1] for result in results if result[0]]
        return item
