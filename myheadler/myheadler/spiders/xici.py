# -*- coding: utf-8 -*-
import scrapy
from myheadler.items import MyheadlerItem


class XiciSpider(scrapy.Spider):
    #爬虫名
    name = 'xici'
    #作用域
    allowed_domains = ['www.xicidaili.com']
    #页码
    offset = 1
    url = 'http://www.xicidaili.com/nt/'
    #开始url，默认会调用parse方法
    start_urls = [url + str(offset)]

    def parse(self, response):
        item = MyheadlerItem()
        #获取除标题的所有tr标签
        ip_list = response.xpath("//tr[node()>1]")
        #遍历得到想要的数据
        for each in ip_list:
            item["ip"] = each.xpath("./td[2]/text()").extract()[0]
            item["port"] = each.xpath("./td[3]/text()").extract()[0]
            addr = each.xpath("./td[4]/a/text()").extract()
            #xpath获取的是列表，第0个就是第一个元素
            if len(addr) != 0:
                item["addr"] = addr[0]
            yield item

        #页码开关，当前是682，这个之后会变动
        if self.offset <= 682:
            self.offset += 1
            yield scrapy.Request(self.url + str(self.offset),callback=self.parse)

