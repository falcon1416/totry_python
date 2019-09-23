# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3,time
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

