# -*- coding: utf-8 -*-

import scrapy

from Amazon.items import AmazonItem
from Amazon.settings import DEFAULT_REQUEST_HEADERS

from bs4 import BeautifulSoup

BASE_URL = 'https://www.amazon.com'


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    page = 1
    keyword = 'oxygen+concentrator'
    start_urls = [
        'https://www.amazon.com/s?k=' + keyword + '&page=' + str(page)]

    def parse(self, response):
        url_list = response.xpath('//a[@title="status-badge"]/@href').extract()
        last = response.xpath('//li[@class="a-last"]').extract()

        product_url_list = [BASE_URL + x for x in url_list]
        # 判断是否是最后一页，是最后一页则结束
        if not last or self.page > 1:
            return

        for product_url in product_url_list:
            yield scrapy.Request(url=product_url,
                                 callback=self._get_product_details,
                                 headers=DEFAULT_REQUEST_HEADERS)
        self.page += 1
        yield scrapy.Request(
            url='https://www.amazon.com/s?k=oxygen+concentrator&page=' + str(
                self.page) + '&ref=is_pn_' + str(self.page - 1),
            callback=self.parse)

    def _get_product_details(self, response):
        title = response.xpath('//span[@id="title"]/text()').extract_first()
        # 产品图片地址
        image_url = response.xpath(
            '//img[@data-fling-refmarker="detail_main_image_block"]/@data-midres-replacement').extract_first()  # noqa: E501
        # 商品唯一标识
        asin = response.xpath(
            '//div[@id="cerberus-data-metrics"]/@data-asin').extract_first()
        # 价格
        price = response.xpath(
            '//div[@id="cerberus-data-metrics"]/@data-asin-price').extract_first()  # noqa: E501
        # 描述
        description = response.xpath(
            '//*[@id="productDescription_fullView"]').extract_first()
        if description:
            # 过滤掉html标签
            description = BeautifulSoup(description).get_text()
        # 特征
        features = response.xpath(
            '//div[@id="feature-bullets"]//span[@class="a-list-item"]/text()')\
            .extract()

        # 如果没有评论也没有获取到产品特征，那就不要这条数据
        if not description and not features:
            return

        item = AmazonItem()
        item['title'] = title
        item['asin'] = asin
        item['image_url'] = image_url
        item['url'] = response.url
        item['price'] = price
        item['description'] = description
        item['features'] = features

        comments_url = 'https://www.amazon.com/kinery-Concentrator-Generator' \
                       '-Adjustable-Humidifiers/product-reviews/%s/ref=cm_cr' \
                       '_unknown?ie=UTF8&reviewerType=all_reviews&filterBy' \
                       'Star=five_star&pageNumber=1' % asin
        yield scrapy.Request(
            url=comments_url, callback=self._get_good_comments,
            meta={"item": item})

    def _get_good_comments(self, response):
        """获取商品好评:只取一页五星好评"""
        review_titles = response.xpath(
            '//span[@data-hook="review-title"]/span/text()').extract()
        review_contents = response.xpath(
            '//div[@aria-expanded="false"]/span/text()').extract()

        item = response.meta["item"]
        item["review_good_titles"] = review_titles
        item["review_good_contents"] = review_contents

        comments_url = 'https://www.amazon.com/kinery-Concentrator-' \
                       'Generator-Adjustable-Humidifiers/product-reviews/%s' \
                       '/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews' \
                       '&filterByStar=one_star&pageNumber=1' % item.get('asin')
        yield scrapy.Request(
            url=comments_url, callback=self._get_bad_comments,
            meta={"item": item})

    def _get_bad_comments(self, response):
        """获取商品差评:只取一页一星差评"""
        review_titles = response.xpath(
            '//span[@data-hook="review-title"]/span/text()').extract()
        review_contents = response.xpath(
            '//div[@aria-expanded="false"]/span/text()').extract()

        item = response.meta["item"]
        item["review_bad_titles"] = review_titles
        item["review_bad_contents"] = review_contents

        yield item
