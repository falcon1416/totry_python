# -*-coding:utf8-*-

import sys,os
import time
from urllib import request
from bs4 import BeautifulSoup

NAME="江苏省科技厅通知公告"
FILE_PATH="./data/"

HOST="http://kxjst.jiangsu.gov.cn"
URL=HOST+"/col/col48967/index.html"

# 查询列表
def getList():
  out_list=[]
  req = request.Request(URL)
  req.add_header('User-Agent', 'Mozilla/6.0')
  response =  request.urlopen(req)
  html=response.read().decode('utf-8')
  # print(html)
  soup = BeautifulSoup(html,"html.parser")
  tbody=soup.find('body').find('div',id='barrierfree_container').find(name='table',attrs={"style":"border-top:4px solid #ffffff"}).find("tbody")
  for tag in tbody.children:
    if tag.name == None:
      continue
    
    for tdTag in tag.children:
      if tdTag.name == None:
        continue
      
      if 'style' not in tdTag.attrs:
        continue
      
      t=tdTag.find('tbody')
      i=0
      for tTag in t.children:
        if tTag.name == None:
          continue
        
        i=i+1
        if i!=2:
          continue
        
        tt=tTag.find('td')
        for ttTag in tt.children:
          if ttTag.name == None:
            continue
          
          if ttTag.name !="table":
            continue
          
          ttrs=ttTag.findAll("tr")
          for aa in ttrs[1].find('td').find('div').children:
            if aa.name == None:
              continue

            a_aa=str(aa).split("<a")
            for i in range(1,len(a_aa)-1):
              buf_a=a_aa[i].split("</a>")
              buf=buf_a[0]
              buf1=buf.split('title="')
              if len(buf1)==1:
                continue
              url=HOST+buf1[0].split('href="')[1].split('"')[0]
              title=buf1[1].split('">')[0]
              out_list.append({"url":url,"title":title})
              # print("url:"+url)
              # print("title:"+title)
              # print("===========")
            
            
          

    return out_list

def getDetail(url):
  out_list=[]
  req = request.Request(url)
  req.add_header('User-Agent', 'Mozilla/6.0')
  response =  request.urlopen(req)
  html=response.read().decode('utf-8')
  soup = BeautifulSoup(html,"html.parser")
  arr=soup.find('body').findAll("p")
  for tag in arr:
    a=tag.find('a')
    if a is None:
      continue
    file_url=HOST+a.get('href')
    file_name=tag.text
    out_list.append({"file_url":file_url,"file_name":file_name})
  return out_list

def download(item):
  today=time.strftime('%Y-%m-%d',time.localtime())
  path=FILE_PATH+today+"/"

  # 创建文件夹
  if os.path.exists(path)==False:
    os.mkdir(path) 
  
  path=path+NAME+"/"
  if os.path.exists(path)==False:
    os.mkdir(path)
  
  path=path+item["title"]+"/"
  if os.path.exists(path)==False:
    os.mkdir(path)
  
  for obj in item["file_list"]:
    file_path=path+obj["file_name"]
    file_url=obj["file_url"]

    print("下载文件:"+file_url)
    print("保存路径:"+file_path)
    request.urlretrieve(file_url,file_path)

def main():
  list=getList()
  
  for item in list:
    print("正在下载:"+item["title"]+","+item["url"])
    url=item["url"]
    item["file_list"]=getDetail(url)

    download(item)
    break
  # print(list)
  
  



if __name__ =='__main__':
  main()