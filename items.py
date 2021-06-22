# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    price_discount = scrapy.Field()
    rate = scrapy.Field()
    updated = scrapy.Field()
    _id = scrapy.Field()
