# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jandan.items import JandanItem
from selenium import webdriver
from bs4 import BeautifulSoup as bs4


class JdSpider(CrawlSpider):
    name = 'jd'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/pic/page-1#comments/']

    rules = (
        Rule(LinkExtractor(allow=r'pic/page-\d+'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = JandanItem()
        driver = webdriver.PhantomJS()
        driver.get(response.url)
        soup = bs4(driver.page_source, 'html.parser')
        all_data = soup.find_all('div', {'class': 'row'})
        for i in all_data:
            # name = each.xpath('.//strong/text()').extract()
            # if len(name) != 0:
            #     item["name"] = name[0]
                # item["jpg_url"] = each.xpath('.//img/@src').extract()
            # item["name"] = each
            # item["url"] = each.get('src')
            # if len(gif_url) != 0:
            #     item["gif_url"] = gif_url
            name = i.find("strong")
            item["name"] = name.get_text().strip()
            link = i.find('a', {'class': 'view_img_link'})
            url = link.get("href")
            if len(url) == 0:
                return
            item["url"] = "http://" + url.split("//")[-1]
            yield item
