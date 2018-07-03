# -*- coding: utf-8 -*-
import scrapy
import urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from nhb.items import NhbItem


class GifSpider(CrawlSpider):
    name = 'gif'
    allowed_domains = ['neihanpa.com']
    start_urls = ['http://www.neihanpa.com/gif/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/index(_\d+)*.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/index(_\d+)*.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        item = NhbItem()
        # item_list = []
        data = response.xpath('//div[@class="pic-column-list mt10"]/div')
        for each in data:
            item["gif_title"] = each.xpath(".//h3/a/@title").extract()[0]
            item["gif_url"] = each.xpath(".//img/@src").extract()[0]
            # item.setdefault("gif_title",[]).append(title)
            # item.setdefault("gif_url", []).append(url)
            # url = response.urljoin(item["imagesUrls"])
            # yield scrapy.Request(url, callback=self.parse_gif)
            yield item

    # def parse_gif(self, response):
    #     body = response.body
    #     for url in body.split("'"):
    #         if (url.startswith("http") and url.endswith(".gif")):
    #             print
    #             "real url is " + url
    #             local = url.split('/')[-1]
    #             urllib.urlretrieve(url, local)