# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FuturespiderItem(scrapy.Item):
    up_time = scrapy.Field()
    position = scrapy.Field()
    pay = scrapy.Field()
    addr = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
