# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    book_name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 状态
    status = scrapy.Field()
    # 周点击量
    # click_rate = scrapy.Field()
    # 月票
    ticket = scrapy.Field()
    # 字数
    word_count = scrapy.Field()
    pass
