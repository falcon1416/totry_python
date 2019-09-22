import re,base64,io,json

class ParseDecode:
  def __init__(self):
    with open('./totry_crawler/ccw.json', 'r') as f:
      self.fontdict = json.load(f)

  def decode(self,buf):
    new_content=""
    for val in buf:
      if '\u4e00' <= val <= '\u9fff':
        uni=val.encode('unicode-escape')
        val_code="uni"+uni[2:].decode('utf-8').upper()
      else:
        val_code="\\"+val.encode('utf-8').hex()
        # print(val_code)

      if val_code in self.fontdict:
        new_content=new_content+self.fontdict[val_code]
      else:
        new_content=new_content+val
    return new_content