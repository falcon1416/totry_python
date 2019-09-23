import sqlite3
import time

class DB:
  def __init__(self):
    self.conn = sqlite3.connect('./totry_crawler/db/totry.db')
    self.cur = self.conn.cursor()
  
  def isHaveByChace(self,menuID):
    self.cur.execute("select * from chacewang where menuID='"+menuID+"'")
    rows=self.cur.fetchall()
    if len(rows)==0:
      return False
    else:
      return True
  
  def addByChace(self,menuID,proejctName,deptName,areaName,seTime,overView,supportFrom):
    self.cur.execute("INSERT INTO chacewang VALUES('"+menuID+"','"+proejctName+"','"+deptName+"','"+areaName+"','"+seTime+"','"+overView+"','"+supportFrom+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"')")
    self.conn.commit()
  
  def getIndexByChace(self):
    self.cur.execute("select `index` from chacewang_log order by create_time desc ")
    row=self.cur.fetchone()
    if row is None:
      return -1
    
    return row[0]
  
  def addLogByChace(self,index):
    self.cur.execute("INSERT INTO chacewang_log(`index`,`create_time`) VALUES('"+str(index)+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"')")
    self.conn.commit()

  def __del__(self):
    self.cur.close()
    self.conn.close()