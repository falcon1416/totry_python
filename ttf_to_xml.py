
#http://fontstore.baidu.com/static/editor/index.html#
from fontTools.ttLib import TTFont
import re,base64,io,json
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

# print(newmap)

# response_="间建罪及共和算"
# for key,value in newmap.items():
#   key_ = key.replace('0x','&#x') + ';'
#   # print(key,key_)
#   if key_ in response_:
#     response_ = response_.replace(key_,str(value))
# print(response_)


newmap = dict()
def parse_font():
  font1 = TTFont('./ccw.ttf')
  keys, values = [], []
  for k, v in font1.getBestCmap().items():
    if v.startswith('uni'):
      newmap["u'\\u{:x}".format(k) + "'"]=chr(int(v[3:], 16))
      keys.append(eval("u'\\u{:x}".format(k) + "'"))
      values.append(chr(int(v[3:], 16)))
    else:
      keys.append("&#x{:x}".format(k))
      values.append(v)
  # print(keys, values)
  return dict(zip(keys, values))
parse_font()
print(newmap)
 

 
# def toUnicode(oneStr):
#   t=oneStr
#   if  t[:3] == 'uni':t=t.replace('uni','\\u') 
#   if  t[:2] == 'uF':t=t.replace('uF','\\u') 
#   return json.loads(f'"{t}"') 

# def printUNI(fontName,imagePath):
#   font = TTFont(fontName)
#   # gs = font.getGlyphSet()
#   glyphNames = font.getGlyphNames()
#   for i in glyphNames:
#       if i[0] == '.':#跳过'.notdef', '.null'
#           continue
#       # print (i)
#       print (i ,toUnicode(i)  )
        
# fontName="ccw.ttf"
# imagePath="images/FSung-F"
# printUNI(fontName,imagePath)

# # 解析字体库
# font = TTFont('ccw.ttf')
# # 读取字体的映射关系,
# uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder() # 参数'cmap' 表示汉字对应的映射 为unicode编码
# print(uni_list)
# #.notdef 并不是汉字的映射， 而是表示字体家族名称。真是数据是从下标 1 开始
# for x in uni_list:
#   print(x)
#   # utf_list = [eval(r"u'\u" + x[3:] + "'") 
# # print(utf_list)

# font = TTFont('ccw.ttf') #打开本地的ttf文件
# bestcmap = font['cmap'].getBestCmap()
# newmap = dict()
# for key in bestcmap.keys():
#   if re.search(r'(\d+)', bestcmap[key]) is None:
#     continue
#   value = int(re.search(r'(\d+)', bestcmap[key]).group(1)) - 1
#   key = hex(key)
#   newmap[key] = value
# print(newmap)

# 解析字体库font文件
# font = TTFont('ccw.ttf')
# uniList = font['cmap'].tables[0].ttFont.getGlyphOrder()
# for uni in uniList[1:]:
#   if len(uni[3:])==0:
#     continue
#   print(uni[3:])
#   print(eval("u'\\u" + uni[3:] + "'"))
# # utf8List = [eval("u'\u" + uni[3:] + "'").encode("utf-8") for uni in uniList[1:]]
# # print(utf8List)