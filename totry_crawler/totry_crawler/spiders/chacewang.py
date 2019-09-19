# -*- coding: utf-8 -*-
import scrapy,time
import json

class ChacewangSpider(scrapy.Spider):
    name = 'chacewang'
    # allowed_domains = ['chacewang.com']
    # start_urls = ['http://chacewang.com/']
    detail_url="http://www.chacewang.com/ProjectSearch/NewPeDetail/"

    # 动态生成初始 URL
    def start_requests(self):
        # print("================")
        t = time.time()
        t=int(round(t * 1000))
        city="RegisterArea_HDDQ_Anhui_HeFei"
        start_url="http://www.chacewang.com/ProjectSearch/FindWithPager?sortField=CreateDateTime&sortOrder=desc&pageindex=0&pageSize=20&cylb=&diqu="+city+"&bumen=&cylbName=&partition=&partitionName=&searchKey=&_="+str(t)
        # print(start_url)
        yield scrapy.Request(url=start_url, callback=self.parse)
        print("================\n\n\n\n\n")

    def parse(self, response):
        # print("================")
        sites = json.loads(response.body_as_unicode())
        rows=sites['rows']
        for row in rows:
            menuID=row['MainID']
            url=self.detail_url+menuID+"?from=home"
            yield scrapy.Request(url=url, callback=self.parse_detail)
            break

        print("================\n\n\n\n\n")
        pass

    def parse_detail(self, response):
        print("================")
        print(response)
        print("================\n\n\n\n\n")
        pass
