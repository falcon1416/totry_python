from fontTools.ttLib import TTFont
import re,base64,io
import requests
from lxml import etree

# font = TTFont('./ccw.ttf')
# bestcmap = font['cmap'].getBestCmap()
# newmap = dict()
# for key in bestcmap.keys():
#   if re.search(r'(\d+)', bestcmap[key]) is None:
#     continue
#   value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
#   key = hex(key)
#   newmap[key] = value

# response_="间建罪及共和算"
# for key,value in newmap.items():
#   key_ = key.replace('0x','&#x') + ';'
#   # print(key,key_)
#   if key_ in response_:
#     response_ = response_.replace(key_,str(value))
# print(response_)



def parse_font():
  font1 = TTFont('./ccw.ttf')
  keys, values = [], []
  for k, v in font1.getBestCmap().items():
    if v.startswith('uni'):
      keys.append(eval("u'\\u{:x}".format(k) + "'"))
      values.append(chr(int(v[3:], 16)))
    else:
      keys.append("&#x{:x}".format(k))
      values.append(v)
  print(keys, values)
  return dict(zip(keys, values))



parse_font()

 