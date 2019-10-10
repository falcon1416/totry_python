# -*- coding: utf-8 -*-
import scrapy,time
import json,os
from totry_crawler.parseDecode import ParseDecode
from totry_crawler.items import Item
from totry_crawler.db.db import DB
from totry_crawler.db.writeCSV import WriteCSV
from totry_crawler.sendemail import SendEmail
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings

class ChacewangSpider(scrapy.Spider):
    name = 'chacewang'
    city_title=""
    cookies={}
    # allowed_domains = ['chacewang.com']
    # start_urls = ['http://chacewang.com/']
    detail_url="http://www.chacewang.com/ProjectSearch/NewPeDetail/"
    
    is_have_data=False

    pDecode=ParseDecode()
    db=DB()
    csv=WriteCSV()

    # 完成
    def close(self,spider, reason):
        print("@@@@@@@@@@@@@@@@@@@@@@")
        # filepath=self.csv.filePath(self.city_title)
        # if reason =='finished':
        #     sEmail=SendEmail()
        #     sEmail.send('查策网['+self.city_title+"]数据",filepath,self.city_title)
        
        # #删除旧的文件
        # if os.path.exists(filepath)==True:
        #     os.remove(filepath)
        print("@@@@@@@@@@@@@@@@@@@@@@")

    # 动态生成初始 URL
    def start_requests(self):
        # 登录
        settings = get_project_settings()
        account=settings.get('USER_ACCOUNT')
        password=settings.get('USER_PASSWORD')
        url=settings.get('LOGIN_URL')
        data={
            "Account":account,
            "EnPassword":password
        }
        yield scrapy.FormRequest(url=url,formdata=data,callback=self.parse_login)
       

    
    #登录解析
    def parse_login(self,response):
        #解析cookie
        cookie=response.request.headers['Cookie'].decode('utf-8')
        print("\n\n@@@@@@@@ cookie:"+cookie+"\n")
        arr=cookie.split('=')
        self.cookies[arr[0]]=arr[1]

        print("查询列表信息\n================")
        settings = get_project_settings()
        url=settings.get('LIST_URL')

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
        
        item=urls[currentIndex]
        self.city_title=item["title"]
        city_code=item["key"]

        pageindex=0
        url=url+str(pageindex)+"&diqu="+city_code+"&_="+str(t)
        print("city_title:"+self.city_title)
        print(url)
        yield scrapy.Request(url=url,cookies=self.cookies, callback=self.parse_list, meta={"city_code":city_code,"pageindex":pageindex},dont_filter=True)
        self.db.addLogByChace(currentIndex)
        print("================\n\n\n\n\n")
        
    #解析列表
    def parse_list(self, response):
        city_code = response.meta['city_code']
        pageindex = response.meta['pageindex']
        print("正在下载 %s(%s) 第%d页" % (self.city_title,city_code,(pageindex+1)))

        sites = json.loads(response.body_as_unicode())
        if 'rows' not in sites:
            return
        rows=sites['rows']
        for row in rows:
            menuID=row['MainID']
            isHave=self.db.isHaveByChace(menuID)
            if isHave==True:
                continue
            
            self.is_have_data=True
            
            #项目名称
            proejctName=row['PEName']
            proejctName=self.pDecode.decode(proejctName)
            #受理部门
            deptName=row['DeptFullName']
            deptName=self.pDecode.decode(deptName)
            #地区
            areaName=row['AreaFullName']
            areaName=self.pDecode.decode(areaName)
            #申报时间
            seTime=row['SETime']
            seTime=self.pDecode.decode(seTime)
            # time_arr=seTime.split("-")
            # startime=""
            # endtime=""
            # if len(time_arr) ==2:
            #     startime=time_arr[0].strip()
            #     endtime=time_arr[1].strip()

            #申报条件
            overView=row['OverView']
            overView=self.pDecode.decode(overView)
            #支持力度
            supportFrom=row['SupportFrom']
            supportFrom=self.pDecode.decode(supportFrom)

            item=Item()
            item["menuID"]=menuID
            item["proejctName"]=proejctName
            item["deptName"]=deptName
            item["areaName"]=areaName+"("+city_code+")"
            item["seTime"]=seTime
            item["overView"]=overView
            item["supportFrom"]=supportFrom

            #结果保存到csv文件
            self.csv.write(self.city_title,item)

            #查询详情
            detail_url=self.detail_url+menuID
            yield scrapy.Request(url=detail_url,cookies=self.cookies, callback=self.parse_detail, meta={"item":item},dont_filter=True)
            # yield item
            

        #检测下一页
        total= sites['total']
        if (pageindex*20+len(rows)) < total:
            #还有下一页
            t = time.time()
            t=int(round(t * 1000))
            pageindex=pageindex+1
            settings = get_project_settings()
            url=settings.get('LIST_URL')
            url=url+str(pageindex)+"&diqu="+city_code+"&_="+str(t)
            yield scrapy.Request(url=url,cookies=self.cookies, callback=self.parse_list, meta={"city_code":city_code,"pageindex":pageindex},dont_filter=True)
    
    def parse_detail(self, response):
        item = response.meta['item']
        selector = Selector(response)
        div = selector.xpath('//div[@class="detail-content project-detail"]')[0]
        sub_divs=div.xpath('div')
        
        for eachdiv in sub_divs:
            title=eachdiv.xpath('p[@class="common-title"]/text()').extract()[0]
            content=""
            if title=="产业类别":
                arr=eachdiv.xpath('ul[@class="list-unstyleds ccw-font-style"]/li/text()').extract()
                for c in arr:
                    content=content+c+"\t"
                content=self.pDecode.decode(content)
                item["estate"]=content
            elif title=="支持力度" or title=="申报材料" or title=="申报条件":
                arr=eachdiv.xpath('p[@class="ccw-font-style"]/text()').extract()
                for c in arr:
                    content=content+c+"\n"
                content=self.pDecode.decode(content)
                if title=="支持力度":
                    item["support"]=content
                if title=="申报材料":
                    item["materials"]=content
                if title=="申报条件":
                    item["condition"]=content
            else:
                arr=eachdiv.xpath('p')
                for i in range(1,len(arr)):
                    c=arr[i]
        
                    if len(c.xpath('a'))==0:
                        if c.xpath('text()') is not None:
                            content=content+c.xpath('text()').extract()[0]+"\n"
                    else:
                        content=content+c.xpath('a/text()').extract()[0]+"\n"
                if title=="项目来源":
                    item["source"]=content
                if title=="申报系统":
                    item["system"]=content
        yield item
            



