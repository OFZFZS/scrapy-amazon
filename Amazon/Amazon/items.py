# -*- coding: utf-8 -*-

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image_url = scrapy.Field()
    asin = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    features = scrapy.Field()
    # 好评
    review_good_titles = scrapy.Field()
    review_good_contents = scrapy.Field()

    # 差评
    review_bad_titles = scrapy.Field()
    review_bad_contents = scrapy.Field()
