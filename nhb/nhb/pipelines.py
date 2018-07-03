# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from urllib import request
import os
import json
import requests
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from scrapy.conf import settings
import pymysql

class NhbPipeline(object):
    # def process_item(self, item, spider):
        # url = item["gif_url"]
        # path = "images/" + item["gif_title"] + ".gif"
        # html = requests.get(url)
        # with open(path, 'wb') as file:
        #     file.write(html.content)
        #将获取的文件另存为
        # request.urlretrieve(item["gif_url"], r'E:\test\images\%s.gif' %item["gif_title"])
        # return item
    # def process_item(self, item, spider):
    #     if 'gif_url' in item:
    #         images = []
    #         dir_path = settings.IMAGES_STORE
    #         path = item["gif_title"] + ".gif"
    #         file_path = '%s/%s' % (dir_path, path)
    #
    #         if not os.path.exists(dir_path):
    #             os.makedirs(dir_path)
    #         if not os.path.exists(file_path):
    #             with open(file_path, 'wb') as handle:
    #                 response = requests.get(item["gif_url"], stream=True)
    #                 for block in response.iter_content(1024):
    #                     if not block:
    #                         break
    #
    #                     handle.write(block)
    #     return item


    #下载到json文件
    # def close_spider(self,spider):
    #     print("！！！！！！！已爬取完毕，nice work！！！！！！！！")
    # def __init__(self):
    #     self.filename = open("nhb.json","wb")
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


    #下载到mysql数据库
    def __init__(self):
        host = settings["MYSQL_HOST"]
        port = settings["MYSQL_PORT"]
        user = settings["MYSQL_USER"]
        passwd = settings["MYSQL_PASSWD"]
        db = settings["MYSQL_DB"]

        self.mysqlcli = pymysql.connect(host=host, port=port,user=user, passwd=passwd, db=db, charset="utf8")
        # 创建mysql 操作游标对象，可以执行mysql语句
        self.cursor = self.mysqlcli.cursor()

    def process_item(self, item, spider):
        try:
            sql = "insert into gif_init(name,url) values (%s,%s)"
            params = [item['gif_title'],item['gif_url']]
            #执行sql语句
            self.cursor.execute(sql,params)
            # 提交事务
            self.mysqlcli.commit()
        except:
            print("数据异常")
        return item

    def close_spider(self,spider):
        # 关闭游标
        self.cursor.close()

    #获取settings文件设置的变量值
    # IMAGES_STORE = get_project_settings().get("IMAGES_STORE")
    #
    # def get_media_requests(self, item, info):
    #     image_url = item["imagesUrls"]
    #     yield scrapy.Request(image_url)
    #
    # def item_completed(self, results, item, info):
    #     # 固定写法，获取图片路径，同时判断这个路径是否正确，如果正确，就放到 image_path里，ImagesPipeline源码剖析可见
    #     image_path = [x["path"] for ok, x in results if ok]
    #
    #     os.rename(self.IMAGES_STORE + "/" + image_path[0], self.IMAGES_STORE + "/" + item["name"] + ".gif")
    #     item["imagesPath"] = self.IMAGES_STORE + "/" + item["name"]

