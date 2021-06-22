from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from spiders.labirint import LabirintruSpider
from spiders.book24 import Book24ruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintruSpider)
    process.crawl(Book24ruSpider)

    process.start()

