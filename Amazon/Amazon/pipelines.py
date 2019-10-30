# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from Amazon.items import AmazonItem

from pymongo import MongoClient


class AmazonGoodsPipeline(object):
    """将商品详情保存到MongoDB"""

    def open_spider(self, spider):
        self.db = MongoClient(host="127.0.0.1", port=27017)
        self.client = self.db.Amazon.Pipa

    def process_item(self, item, spider):
        if isinstance(item, AmazonItem):
            _item = dict(item)
            _item['_id'] = _item['asin']
            try:
                # asin作为主键,插入重复会报错
                self.client.insert(_item)
            except Exception as err:
                pass

        return item
