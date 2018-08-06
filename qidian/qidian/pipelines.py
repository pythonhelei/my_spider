# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from pymongo import MongoClient

class QidianPipeline(object):

    def __init__(self):
        host = settings['MONGO_HOST']
        port = settings['MONGO_PORT']
        dbname = settings['MONGO_DBNAME']
        colname = settings['MONGO_COLNAME']
        self.client = MongoClient(host, port)
        self.db = self.client[dbname]
        self.col = self.db[colname]

    def process_item(self, item, spider):
        data = dict(item)
        self.col.insert(data)
        return item

    def __del__(self):
        self.client.close()
