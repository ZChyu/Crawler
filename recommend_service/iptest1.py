# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:05:19 2018

@author: Zcy
"""

from urllib import request
 
#爬嗅事百科
url='https://www.baidu.com'
#写入User-Agent，采用字典形式
head={}
head['User-Agent']='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
#创建Request对象并添加heads
req=request.Request(url,headers=head)
#传入创建好的Request对象
response=request.urlopen(req)
#读取响应信息并解码
html=response.read().decode('utf-8')
#打印爬到的信息
print(html)