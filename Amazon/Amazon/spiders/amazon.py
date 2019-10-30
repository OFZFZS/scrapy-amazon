# -*- coding: utf-8 -*-

import scrapy
import requests

from Amazon.items import AmazonItem
from Amazon.settings import DEFAULT_REQUEST_HEADERS

from bs4 import BeautifulSoup

BASE_URL = 'https://www.amazon.com'


class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    page = 1
    lost_item = 0
    keyword = 'Pipa'
    rh = 'n%3A11091801'
    cookies = {
        "anonymid": "j7wsz80ibwp8x3",
        "_r01_": "1",
        "ln_uact": "mr_mao_hacker@163.com",
        "_de": "BF09EE3A28DED52E6B65F6A4705D973F1383380866D39FF5",
        "depovince": "GW",
        "jebecookies": "2fb888d1-e16c-4e95-9e59-66e4a6ce1eae|||||",
        "ick_login": "1c2c11f1-50ce-4f8c-83ef-c1e03ae47add",
        "p": "158304820d08f48402be01f0545f406d9",
        "first_login_flag": "1",
        "ln_hurl": "http://hdn.xnimg.cn/photos/hdn521/20180711/2125/main_SDYi_ae9c0000bf9e1986.jpg",
        "t": "adb2270257904fff59f082494aa7f27b9",
        "societyguester": "adb2270257904fff59f082494aa7f27b9",
        "id": "327550029",
        "xnsid": "4a536121",
        "loginfrom": "syshome",
        "wp_fold": "0"
    }

    headers = {
        'Host': 'www.amazon.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; \
                        SM-A520F Build/NRD90M; wv) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Version/4.0 \
                        Chrome/65.0.3325.109 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,\
                        application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }

    def start_requests(self):
        """
            start_requests做为程序的入口，可以重写，自定义第一批请求
            可以添加headers、cookies, , dont_filter=True
        """
        start_urls = [
            'https://www.amazon.com/s?k=' + self.keyword + '&page=' + str(
                self.page) + '&rh=' + self.rh,
            # 'https://www.amazon.com/s?k=' + keyword + '&page=' + str(page)+'&rh=n%3A1055398'
        ]

        for url in start_urls:
            yield scrapy.Request(url, headers=self.headers,
                                 callback=self.parse)

    def parse(self, response):
        url_list = response.xpath('//a[@title="status-badge"]/@href').extract()
        last = response.xpath('//li[@class="a-last"]').extract()

        product_url_list = [BASE_URL + x for x in url_list]
        # 判断是否是最后一页，是最后一页则结束

        if not last or self.page >= 5:
            print('翻页结束,当前页:%s 没有描述特征商品数:%s' % (self.page, self.lost_item))
            return

        for product_url in product_url_list:
            yield scrapy.Request(url=product_url,
                                 callback=self._get_product_details,
                                 headers=DEFAULT_REQUEST_HEADERS)
        self.page += 1
        yield scrapy.Request(
            url='https://www.amazon.com/s?k=' + self.keyword + '&page=' + str(
                self.page) + '&rh=' + self.rh + '&ref=is_pn_' + str(self.page -
                                                                    1),
            callback=self.parse)

    def _get_product_details(self, response):
        # 处理亚马逊的反爬文本,释放注释代码
        res_body = response.text
        _res = res_body.replace('<!--rbd-->', '').replace('<!-->', '')
        response = response.replace(body=_res)

        title = response.xpath('//span[@id="title"]/text()').extract_first()
        if not title:
            print('您的IP已被亚马逊限制,请更换IP后重试')
            return
        title = title.replace('\n', '')
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
            '//div[@id="feature-bullets"]//span[@class="a-list-item"]/text()') \
            .extract()

        # 如果没有评论也没有获取到产品特征，那就不要这条数据
        if not description and not features:
            self.lost_item += 1
            print('没有描述也没有特征,结束..,总共已过滤%s个' % self.lost_item)
            return

        item = AmazonItem()
        item['title'] = title
        item['asin'] = asin
        item['image_url'] = image_url
        item['url'] = response.url
        item['price'] = price
        item['description'] = description
        item['features'] = features

        # 保存图片
        try:
            self.save_image(image_url, asin)
        except Exception:
            print('图片下载保存失败..')

        comments_url = 'https://www.amazon.com/kinery-Concentrator-Generator' \
                       '-Adjustable-Humidifiers/product-reviews/%s/ref=cm_cr' \
                       '_unknown?ie=UTF8&reviewerType=all_reviews&filterBy' \
                       'Star=five_star&pageNumber=1' % asin
        yield scrapy.Request(
            url=comments_url, callback=self._get_good_comments,
            meta={"item": item})

    def save_image(self, img_url, img_name):
        response = requests.get(img_url)
        # 获取的文本实际上是图片的二进制文本
        img = response.content
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        # 保存路径
        path = '../images/%s.jpg' % (img_name)
        with open(path, 'wb') as f:
            f.write(img)

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
