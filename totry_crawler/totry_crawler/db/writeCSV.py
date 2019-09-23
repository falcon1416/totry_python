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
    filename=self.filePath(filename)
    #删除旧的文件
    if os.path.exists(filename)==True:
      os.remove(filename)

    with open(filename, 'a', encoding='utf-8-sig') as fp:
        writer = csv.writer(fp)
        writer.writerow(data_csv)
  
  def filePath(self,filename):
    return self.dir+"/"+filename+".csv"