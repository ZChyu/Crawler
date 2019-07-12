# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:55:45 2018

@author: Zcy
"""

import urllib.request
import http.cookiejar
import ipProxy
import requests
url = "http://www.nongnet.com"
# 以字典的形式设置headers
headers = {
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #        "Accept-Encoding": "gzip, deflate, br"
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            
            "Host": "www.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    
}
#设置cookie
s = requests.Session()
req = s.get(url=url,headers=headers)
print('--------',s.cookies)
cjar = http.cookiejar.CookieJar()
ip = ipProxy.getProxy()
proxy = urllib.request.ProxyHandler(ip)
opener = urllib.request.build_opener(proxy,urllib.request.HTTPCookieProcessor(cjar))
# 建立空列表，为了以制定格式存储头信息
headall = []
for key,value in headers.items():
    item = (key, value)
    headall.append(item)
# 将制定格式的headers信息添加好
opener.addheaders = headall
# 将opener安装为全局
urllib.request.install_opener(opener)
res =  urllib.request.Request(url)
data = urllib.request.urlopen(res).read()
data = data.decode("utf-8")
print(data)