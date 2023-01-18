# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib

import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline


class ParseLeroyMerlinPipeline:
    def process_item(self, item, spider):
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
