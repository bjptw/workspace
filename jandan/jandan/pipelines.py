# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import requests
from scrapy.conf import settings

class JandanPipeline(object):
    # def __init__(self):
    #     self.filename = open("jandan.json","wb")
    #     self.num = 0
    #
    # def process_item(self, item, spider):
    #     text = json.dumps(dict(item),ensure_ascii=False) + "\n"
    #     self.filename.write(text.encode("utf-8"))
    #     self.num += 1
    #     return item
    #
    # def close_spider(self,spider):
    #     self.filename.close()
    #     print("总共有" + str(self.num) + "个资源")


    def process_item(self, item, spider):
         if 'url' in item:
            dir_path = settings["IMAGES_STORE"]
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            # file_path = '%s/%s' % (dir_path, item["mm_class"])
            # if not os.path.exists(file_path):
            #     os.makedirs(file_path)
            su = "." + item["url"].split(".")[-1]
            path = item["name"] + su
            new_path = '%s/%s' % (dir_path, path)
            if not os.path.exists(new_path):
                with open(new_path, 'wb') as handle:
                    response = requests.get(item["url"], stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break

                        handle.write(block)
            return item
