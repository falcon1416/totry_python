# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3,time
import pymysql
from scrapy.utils.project import get_project_settings
from totry_crawler.parseZoneLevel import ParseZoneLevel

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
        
        # print(item)
        seTime=item["seTime"]
        time_arr=seTime.split("-")
        startime=None
        endtime=None
        if len(time_arr) ==2:
            startime=time_arr[0].strip().replace(".", "-")
            endtime=time_arr[1].strip().replace(".", "-")
        
        pLevel=ParseZoneLevel()
        areaInfo=pLevel.decode(item["areaName"])
        # print(areaInfo)

        if "estate" not in item:
            item["estate"]=""
        else:
            item["estate"]=item["estate"].replace("'", "\'")

        if "materials" not in item:
            item["materials"]=""
        else:
            item["materials"]=item["materials"].replace("'", "\'")

        if "support" not in item:
            item["support"]=""
        else:
            item["support"]=item["support"].replace("'", "\'")

        if "system" not in item:
            item["system"]=""
        else:
            item["system"]=item["system"].replace("'", "\'")

        if "source" not in item:
            item["source"]=""
        else:
            item["source"]=item["source"].replace("'", "\'")

        if "condition" not in item:
            item["condition"]=""
        else:
            item["condition"]=item["condition"].replace("'", "\'")

        if startime is not None:
            sql="insert into project(`_id`,`name`,`dept`,`level`,`province`,`city`,`area`,`zone`,`startime`,`endtime`,`estate`,`condition`,`materials`,`support`,`system`,`source`,`create_time`)"
            sql=sql+"value('"+menuID+"','"+item["proejctName"]+"','"+item["deptName"]+"','"+areaInfo["level"]+"','"+areaInfo["province"]+"','"+areaInfo["city"]+"','"+areaInfo["area"]+"','"+item["areaName"]+"','"+startime+"','"+endtime+"','"+item["estate"].strip()+"','"+item["condition"].strip()+"','"+item["materials"].strip()+"','"+item["support"].strip()+"','"+item["system"].strip()+"','"+item["source"].strip()+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"')"
        else:
            sql="insert into project(`_id`,`name`,`dept`,`level`,`province`,`city`,`area`,`zone`,`estate`,`condition`,`materials`,`support`,`system`,`source`,`create_time`)"
            sql=sql+"value('"+menuID+"','"+item["proejctName"]+"','"+item["deptName"]+"','"+areaInfo["level"]+"','"+areaInfo["province"]+"','"+areaInfo["city"]+"','"+areaInfo["area"]+"','"+item["areaName"]+"','"+item["estate"].strip()+"','"+item["condition"].strip()+"','"+item["materials"].strip()+"','"+item["support"].strip()+"','"+item["system"].strip()+"','"+item["source"].strip()+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"')"
        print("\n\n===================")
        print(sql)
        print("===================\n\n")
        self.cur.execute(sql)

     