# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from futurespider.items import FuturespiderItem


class JobSpider(RedisCrawlSpider):
    name = 'job'
    set_month = 7
    day = 13
    set_day = day - 3
    url_list = []
    # allowed_domains = ['search.51job.com']
    # start_urls = ['http://search.51job.com/']
    redis_key = 'futurespider:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'python%25E5%25BC%2580%25E5%258F%2591,2,\d+.html?'), callback='parse_item', follow=True),
    )
    # 可选：等效于allowd_domains()，__init__方法按规定格式写，使用时只需要修改super()里的类名参数即可
    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #
    #     # 修改这里的类名为当前类名
    #     super(JobSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = FuturespiderItem()
        # page = response.xpath('//span[@class="td"][1]/text()').extract()[0]
        # self.set_page = re.findall(r"\d+",page)[0]
        data = response.xpath('//div[@id="resultList"]/div[@class="el"]')
        for each in data:
            pay = each.xpath('.//span[@class="t4"]/text()').extract()
            url = each.xpath('.//p//a/@href').extract()[0]
            if len(pay) == 0 or url in self.url_list:
                continue
            up_time = each.xpath('.//span[@class="t5"]/text()').extract()[0]
            month = int(up_time.split("-")[0])
            day = int(up_time.split("-")[-1])
            if month == self.set_month and day >= self.set_day:
                item["up_time"] = "2018-" + up_time
                item["position"] = each.xpath('.//p//a/@title').extract()[0]
                item["pay"] = pay[0]
                item["addr"] = each.xpath('.//span[@class="t3"]/text()').extract()[0]
                item["name"] = each.xpath('./span/a/@title').extract()[0]
                self.url_list.append(url)
                item["url"] = url
                yield item
            else:
                break
        # if self.flag:
        #     if self.offset <= self.set_page:
        #         self.offset += 1
        #         yield scrapy.Request(self.front + str(self.offset + self.behind),callback=self.parse)