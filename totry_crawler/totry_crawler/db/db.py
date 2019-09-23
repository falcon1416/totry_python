import sqlite3

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
  
  def addByChace(self,menuID):
    self.cur.execute("INSERT INTO chacewang VALUES('"+menuID+"')")
    self.conn.commit()

  def __del__(self):
    self.cur.close()
    self.conn.close()