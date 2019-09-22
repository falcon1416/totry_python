
#http://fontstore.baidu.com/static/editor/index.html#
# https://blog.csdn.net/qq_42293758/article/details/89644453
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


# newmap = dict()
# def parse_font():
#   font1 = TTFont('./ccw.ttf')
#   keys, values = [], []
#   for k, v in font1.getBestCmap().items():
#     if v.startswith('uni'):
#       newmap["u'\\u{:x}".format(k) + "'"]=chr(int(v[3:], 16))
#       keys.append(eval("u'\\u{:x}".format(k) + "'"))
#       values.append(chr(int(v[3:], 16)))
#     else:
#       keys.append("&#x{:x}".format(k))
#       values.append(v)
#   # print(keys, values)
#   return dict(zip(keys, values))
# parse_font()
# print(newmap)
 

 
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

# response_="&#x95f4;"
# for key,value in newmap.items():
#     key_ = key.replace('0x','&#x') + ';'
#     if key_ in response_:
#       print(key,key_,value)
#       response_ = response_.replace(key_,str(value))
# print(response_)




# print("间".encode('unicode-escape'))
# print(b'9'.hex())



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

# content="间建罪及共和算9"
# for val in content:
#   uni=val.encode('unicode-escape')
#   val_code=uni[2:].decode('utf-8').upper()
#   print(val_code)
#   print("==========")


# font2=TTFont('ccw.ttf')
# uni_list2=font2.getGlyphOrder()[1:]
# on_p1=[]
# for i in uni_list2:
#     pp1 = []
#     p=font2['glyf'][i].coordinates
#     for f in p:
#         pp1.append(f)
#     on_p1.append(pp1)
# print(on_p1)

# onlineFonts = TTFont('ccw.ttf')
# uni_list = onlineFonts.getGlyphNames()[1:-1]
# print(len(uni_list))
# # 解析字体库
# for i in range(100):
#     # onlineGlyph = onlineFonts['glyf'][uni_list[i]]
#     print(uni_list[i][3:].lower() )


##########################################

with open('ccw.json', 'r') as f:
  fontdict = json.load(f)

content="间建罪及共和算6"
new_content=""
for val in content:
  if '\u4e00' <= val <= '\u9fff':
    uni=val.encode('unicode-escape')
    val_code="uni"+uni[2:].decode('utf-8').upper()
  else:
    val_code="\\"+val.encode('utf-8').hex()
    print(val_code)

  if val_code in fontdict:
    new_content=new_content+fontdict[val_code]
  else:
    new_content=new_content+val
print(new_content)

# print("间".encode('unicode-escape'))

# font = TTFont('ccw.ttf')
# font_map = {}  # 用于存储当前页面所使用的自定义字体映射的字典
# for key, value in font.getBestCmap().items():   # 使用getBestCmap()获取字体文件中包含的映射关系
#   if value.startswith('uni'):   # 判断是否是uni编码
#     # print(key,value,chr(int(value[3:], 16)))
#     font_map[hex(key).upper()] =  chr(int(value[3:], 16))   # 这里的upper需看网页中显示的代码点是否是大写的，如果是小写的话，就不需要使用这个了 
#   else:
#     font_map[hex(key).upper()] = value
# # print(font_map)

# for key, value in font_map.items():   # 根据之前得到的{name:真实数据}映射，将font_map中的name进行替换
#   print(key,value)
#   if value in fontdict:
#     font_map[key] = fontdict[value]
# print(font_map)
##########################################