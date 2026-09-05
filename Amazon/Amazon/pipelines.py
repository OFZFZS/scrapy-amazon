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
        """
        在爬虫启动时建立 MongoDB 客户端并选择商品集合。

        :param spider: 当前 Scrapy 爬虫实例
        :return: None
        """
        self.db = MongoClient(host="127.0.0.1", port=27017)
        self.client = self.db.Amazon.Pipa

    def process_item(self, item, spider):
        """
        将 Amazon 商品条目写入 MongoDB，并返回原始条目。

        :param item: 当前抓取到的 Scrapy 条目
        :param spider: 当前 Scrapy 爬虫实例
        :return: 原始 Scrapy 条目
        """
        if isinstance(item, AmazonItem):
            _item = dict(item)
            _item['_id'] = _item['asin']
            try:
                # asin作为主键,插入重复会报错
                self.client.insert_one(_item)
            except Exception as err:
                pass

        return item
