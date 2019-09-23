# -*- coding: utf-8 -*-
import scrapy,time
import json
from totry_crawler.parseDecode import ParseDecode
from totry_crawler.items import Item
from totry_crawler.db.db import DB
from totry_crawler.db.writeCSV import WriteCSV

class ChacewangSpider(scrapy.Spider):
    name = 'chacewang'
    # allowed_domains = ['chacewang.com']
    # start_urls = ['http://chacewang.com/']
    detail_url="http://www.chacewang.com/ProjectSearch/NewPeDetail/"
    
    pDecode=ParseDecode()
    db=DB()
    csv=WriteCSV()

    # 动态生成初始 URL
    def start_requests(self):
        # print("================")
        t = time.time()
        t=int(round(t * 1000))

        #获取城市key
        urls=[]
        with open('./totry_crawler/city.json', 'r') as f:
            urls = json.load(f)
        #计算需要爬的哪个key
        currentIndex=self.db.getIndexByChace()
        currentIndex=currentIndex+1
        if currentIndex >=len(urls):
            currentIndex=0
        
        city_key=urls[currentIndex]["key"]
        city_title=urls[currentIndex]["title"]
        city=city_key
        
        start_url="http://www.chacewang.com/ProjectSearch/FindWithPager?sortField=CreateDateTime&sortOrder=desc&pageindex=0&pageSize=20&cylb=&diqu="+city+"&bumen=&cylbName=&partition=&partitionName=&searchKey=&_="+str(t)
        # print(start_url)
        yield scrapy.Request(url=start_url, callback=self.parse, meta={'title': city_title})
        self.db.addLogByChace(currentIndex)
        print("================\n\n\n\n\n")

    def parse(self, response):
        title = response.meta['title']

        # print("================")
        sites = json.loads(response.body_as_unicode())
        rows=sites['rows']
        for row in rows:
            menuID=row['MainID']
            isHave=self.db.isHaveByChace(menuID)
            if isHave==True:
                continue

            #项目名称
            proejctName=row['PEName']
            proejctName=self.pDecode.decode(proejctName)
            print("项目名称:"+proejctName)
            #受理部门
            deptName=row['DeptFullName']
            deptName=self.pDecode.decode(deptName)
            print("受理部门:"+deptName)
            #地区
            areaName=row['AreaFullName']
            areaName=self.pDecode.decode(areaName)
            print("地区:"+areaName)
            #申报时间
            seTime=row['SETime']
            seTime=self.pDecode.decode(seTime)
            print("申报时间:"+seTime)
            #申报条件
            overView=row['OverView']
            overView=self.pDecode.decode(overView)
            print("申报条件:"+overView)
            #支持力度
            supportFrom=row['SupportFrom']
            supportFrom=self.pDecode.decode(supportFrom)
            print("申报条件:"+supportFrom)

            self.db.addByChace(menuID,proejctName,deptName,areaName,seTime,overView,supportFrom)

            item=Item()
            item["menuID"]=menuID
            item["proejctName"]=proejctName
            item["deptName"]=deptName
            item["areaName"]=areaName
            item["seTime"]=seTime
            item["overView"]=overView
            item["supportFrom"]=supportFrom
            yield item
            
            self.csv.write(title,item)
            # url=self.detail_url+menuID+"?from=home"
            # yield scrapy.Request(url=url, callback=self.parse_detail)
            # break

        print("================\n\n\n\n\n")
        pass

    def parse_detail(self, response):
        print("================")
        print(response)
        print("================\n\n\n\n\n")
        pass
