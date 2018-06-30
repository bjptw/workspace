# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from myheadler.items import MyheadlerItem


class YouheadlerSpider(CrawlSpider):
    name = 'youheadler'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1']

    rules = (
        #规则，参数顺序列表，匹配的规则，回调函数，是否深入
        Rule(LinkExtractor(allow=r'/nn/\d+'), callback='parse_item'),
    )

    def parse_item(self, response):
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item = MyheadlerItem()
        ip_list = response.xpath("//tr[node()>2]")
        for each in ip_list:
            item["ip"] = each.xpath("./td[2]/text()").extract()[0]
            item["port"] = each.xpath("./td[3]/text()").extract()[0]
            addr = each.xpath("./td[4]/a/text()").extract()
            if len(addr) != 0:
                item["addr"] = addr[0]
            yield item

