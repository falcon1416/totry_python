# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3,time
import pymysql
from scrapy.utils.project import get_project_settings

class TotryCrawlerPipeline(object):
  
    def open_spider(self, spider):
        settings = get_project_settings()
        path=settings.get('DB_PATH')
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        menuID=item["menuID"]
        self.cur.execute("select * from chacewang where menuID='"+menuID+"'")
        rows=self.cur.fetchall()
        if len(rows)>0:
            return item

        #添加
        self.cur.execute("INSERT INTO chacewang VALUES('"+item["menuID"]+"','"+item["proejctName"]+"','"+item["deptName"]+"','"+item["areaName"]+"','"+item["seTime"]+"','"+item["overView"]+"','"+item["supportFrom"]+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"')")
        self.conn.commit()

        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

class TotryCrawlerMySQLPipeline:
    def open_spider(self, spider):
        # 连接数据库
        settings = get_project_settings()
        self.connect = pymysql.connect(
            host=settings.get('MYSQL_HOST'),
            port=settings.get('MYSQL_PORT'),
            db=settings.get('MYSQL_DBNAME'),
            user=settings.get('MYSQL_USER'),
            passwd=settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)
        self.cur = self.connect.cursor()
        self.connect.autocommit(True)
    
    def close_spider(self, spider):
        self.cur.close()
        self.connect.close()
    
    def process_item(self, item, spider):
        menuID=item["menuID"]
        self.cur.execute("select * from project where _id='"+menuID+"'")
        rows=self.cur.fetchall()
        if len(rows)>0:
            return item