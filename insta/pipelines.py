import scrapy
from scrapy.pipelines.images import ImagesPipeline


class InstaPipeline:
    def process_item(self, item, spider):
        print(item)
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
