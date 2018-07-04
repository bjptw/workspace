# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import requests
import pymysql
from scrapy.conf import settings

class MyheadlerPipeline(object):
    def __init__(self):
        self.filename = open("xici.json","wb")
        self.num = 0

    def process_item(self, item, spider):
        server = "http://" + item["ip"] + ":" + item["port"]
        try:
            proxy_ip = requests.get('https://www.ipip.net/', proxies={"https": server}, timeout=2)
        except:
            print('connect failed——————' + item["ip"])
        else:
            # print('success' + server)
            self.num += 1
            text = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.filename.write(text.encode("utf-8"))
            print("偷偷爬到第" + str(self.num) + "个ip")
        return item

    def close_spider(self,spider):
        self.filename.close()


    # def __init__(self):
    #     host = settings["MYSQL_HOST"]
    #     port = settings["MYSQL_PORT"]
    #     user = settings["MYSQL_USER"]
    #     passwd = settings["MYSQL_PASSWD"]
    #     db = settings["MYSQL_DB"]
    #
    #     self.mysqlcli = pymysql.connect(host=host, port=port,user=user, passwd=passwd, db=db, charset="utf8")
    #     # 创建mysql 操作游标对象，可以执行mysql语句
    #     self.cursor = self.mysqlcli.cursor()
    #
    # def process_item(self, item, spider):
    #     try:
    #         sql = "insert into headlerip(ip,port,addr) values (%s,%s,%s)"
    #         params = [item['ip'],item['port'],item["addr"]]
    #         #执行sql语句
    #         self.cursor.execute(sql,params)
    #         # 提交事务
    #         self.mysqlcli.commit()
    #     except:
    #         print("数据异常")
    #     return item
    #
    # def close_spider(self,spider):
    #     # 关闭游标
    #     self.cursor.close()