import re,base64,io,json
from xpinyin import Pinyin

class ParseZoneLevel:
  def __init__(self):
    with open('./totry_crawler/zone.json', 'r') as f:
      self.zonelevel = json.load(f)
  
  def decode(self,area):
    p = Pinyin()
    print("\n\n\n\n\n zone_level_area  :"+area)

    for province in self.zonelevel:
      children=province["children"]
      for city in children:
        value=city["value"]
        if value in area:
          return {"province":province["value"],"city":value,"area":"","level":"3"}
    
    for province in self.zonelevel:
      value=province["value"]
      if value in area:
        return {"province":value,"city":"","area":"","level":"2"}

    if "中华人民共和国" in area:
      return {"province":"","city":"","area":"","level":"1"}
    
    for province in self.zonelevel:
      children=province["children"]
      province_name=province["value"]
      for city in children:
        city_name=city["value"]
        city_name_py="_"+p.get_pinyin(province_name,'')+"_"+p.get_pinyin(city_name,'')
        print("city_name_py:"+city_name_py.lower()+"  "+ area.lower())
        if city_name_py.lower() in area.lower():
          area_name=area.split("(")[0]
          return {"province":province_name,"city":city_name,"area":area_name,"level":"4"}
    
    return {"province":"","city":"","area":"","level":"4"}
