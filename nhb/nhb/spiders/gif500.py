# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nhb.items import NhbItem


class Gif500Spider(CrawlSpider):
    name = 'gif500'
    allowed_domains = ['neihanpa.com']
    start_urls = ['http://www.neihanpa.com/e/action/ListInfo/?classid=25&page=500']

    rules = (
        Rule(LinkExtractor(allow=r'&page=\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = NhbItem()
        # item_list = []
        data = response.xpath('//div[@class="pic-column-list mt10"]/div')
        for each in data:
            item["gif_title"] = each.xpath(".//h3/a/@title").extract()[0]
            item["gif_url"] = each.xpath(".//img/@src").extract()[0]
            yield item
