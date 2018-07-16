#coding=utf-8

import redis
import pymysql
import json

def process_item():
# 创建redis数据库连接
    rediscli = redis.Redis(host = "127.0.0.1", port = 6379, db = 0)

# 创建mysql数据库连接
    mysqlcli = pymysql.connect(host = "192.168.1.253", port = 3306,user = "root", passwd = "01", db = "job_51",charset="utf8")

    offset = 0

    while True:
        # 将数据从redis里pop出来
        source, data = rediscli.blpop("job:items")
        item = json.loads(data)
        try:
            # 创建mysql 操作游标对象，可以执行mysql语句
            cursor = mysqlcli.cursor()
            sql = "insert into position_51(up_time,position,pay,addr,name,url) values (%s,%s,%s,%s,%s,%s)"
            params = [item['up_time'],item['position'],item["pay"],item["addr"],item["name"],item["url"]]
            cursor.execute(sql,params)
            # 提交事务
            mysqlcli.commit()
            # 关闭游标
            cursor.close()
            offset += 1
            print(offset)
        except:
            print(item['up_time'],item['position'],item["pay"],item["addr"],item["name"],item["url"])

if __name__ == '__main__':
    process_item()