# -*- coding: utf-8 -*-
import scrapy
from crawler.items import FileItem
import sys,os,time

class SpiderJiangsuGovSpider(scrapy.Spider):
    name = 'spider_jiangsu_gov'
    dommain='http://kxjst.jiangsu.gov.cn'
    # allowed_domains = ['http://kxjst.jiangsu.gov.cn']
    start_urls = ['http://kxjst.jiangsu.gov.cn/col/col48967/index.html']

    DIR_NAME="江苏省科技厅通知公告"
    FILE_PATH="./data/"

    def parse(self, response):
        table=response.xpath("//table")[7] 
        trs = table.xpath('//tr')
        tr=trs[0]
        
        html=tr.extract()
        res=html.split("<record>")
        for record in res:
            record=record.split("</record>")[0]
            a_array=record.split("<a")
            if len(a_array)==1:
                continue
            a_html=a_array[1]
            a_html=a_html.split("</a>")[0]

            buf1=a_html.split('title="')
            if len(buf1)==1:
                continue
            url=self.dommain+buf1[0].split('href="')[1].split('"')[0]
            title=buf1[1].split('">')[0]
            # print(url)
            # print(title)
            
            yield scrapy.Request(url, callback=self.parse_detail, meta={'title': title})
            # print("-----------\n\n")
            # break 

        
        # print("=========================\n\n\n\n\n\n")
        pass
    
    def parse_detail(self, response):
        title = response.meta['title']

        ps=response.xpath("//p/a")
        fileList=[]
        for p in ps:
            name=p.xpath('text()')
            if len(name)==0:
                continue

            name=name.extract()[0]
            url=self.dommain+p.xpath('@href').extract()[0]
            fileList.append({"name":name,"url":url})
            print(name)
            print(url)
            yield scrapy.Request(url=url,callback=self.download,meta={'name':name,'title':title})
            print("@@@@@@@@@\n\n")
        
        item=FileItem()
        item["list"]=fileList
        item["title"]=title
        yield item
        print("=========================\n\n\n\n\n\n")
    
    def download(self, response):
        title = response.meta['title']
        name = response.meta['name']

        today=time.strftime('%Y-%m-%d',time.localtime())
        path=self.FILE_PATH+today+"/"

        # 创建文件夹
        if os.path.exists(path)==False:
            os.mkdir(path) 
        
        path=path+self.DIR_NAME+"/"
        if os.path.exists(path)==False:
            os.mkdir(path)
        
        path=path+title+"/"
        if os.path.exists(path)==False:
            os.mkdir(path)
        
        file_path=path+name
        print("保存路径:"+file_path)

        with open(file_path,'wb') as f:
            f.write(response.body)
        f.close()