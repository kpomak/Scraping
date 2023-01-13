from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from vacancy_scrap import settings as vacancy_settings
from vacancy_scrap.spiders.headhunter import HeadhunterSpider
from vacancy_scrap.spiders.superjob import SuperjobSpider

if __name__ == "__main__":
    settings = Settings()
    settings.setmodule(vacancy_settings)

    process = CrawlerProcess(settings)
    process.crawl(HeadhunterSpider)
    process.crawl(SuperjobSpider)

    process.start()
