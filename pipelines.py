# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pprint import pprint
import pymongo


class BooksPipeline:
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.mongodb = client['books_db']

    def process_item(self, item, spider):
        collection = self.mongodb[spider.name]
        pprint(item)
        collection.find_and_modify({"link": item['link']}, {"$set": item}, upsert=True)
        return item
