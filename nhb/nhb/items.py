# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NhbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 添加字段
    gif_title = scrapy.Field()
    gif_url = scrapy.Field()
    # images = scrapy.Field()
