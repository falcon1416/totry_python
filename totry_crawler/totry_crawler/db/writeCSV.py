import time,os,csv

class WriteCSV:
  def __init__(self):
    subdir=time.strftime("%Y%m%d", time.localtime())
    self.dir='./data/'+subdir

    # 创建文件夹
    if os.path.exists(self.dir)==False:
        os.mkdir(self.dir)
  
  def write(self,filename,item):
    data_csv=[item["proejctName"],item["deptName"],item["areaName"],item["seTime"],item["overView"],item["supportFrom"]]
    filename=self.dir+"/"+filename+".csv"
    with open(filename, 'a', encoding='utf-8') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_csv)