# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 09:55:45 2018

@author: Zcy
"""

import urllib.request
import http.cookiejar

#url = "http://www.nongnet.com/xinxi/323280.aspx"
# 以字典的形式设置headers
def gethtml(url):
    headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #        "Accept-Encoding": "gzip, deflate, br"
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "BAIDUID=CB6C271B385E24C3F8D16B564B186576:FG=1; BIDUPSID=CB6C271B385E24C3F8D16B564B186576; PSTM=1524480879; BD_UPN=12314353; MCITY=-236%3A; BDUSS=DFuTHRuTTFzWnduY0ZFVTNYV355UTVySzB1RTNPMHFJTGRJOWt0VUpDOXhEZkZiQVFBQUFBJCQAAAAAAAAAAAEAAAD~OF1Yu8rJz7vKyc-7ysnPaQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHGAyVtxgMlbN; ispeed_lsm=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=951049216; BD_HOME=1; H_PS_PSSID=26524_1466_21126_27401_22159; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; BD_CK_SAM=1; PSINO=2; shifen[90894435592_78633]=1540948262; BCLID=12384542139186567444; BDSFRCVID=IXDsJeC6269XJMv7dDAm-EDbEg2j9VoTH6aoXhZjnSZB79N8rVl8EG0PjM8g0KubvWn8ogKKymOTHr7P; H_BDCLCKID_SF=tJIfVC-KJD83j-bmKKT0M-FjMfQXKPo0aIKX3buQWxnUqpcNLTDKj6FRy4cqt-3R0CDLKlbt3R0KjCTKhpO1j4_eWM7zat6gyeufVluy-fQSbh5jDh38XjksD-Rt5J5UaJby0hvcMR6cShn4jp00-nDSHH8JJ5-j3f; H_PS_645EC=d66bqq6sFLE7Suw38PGHePXYMVwaM%2FVWBtnQz2FeiBDCVaO2oUw2sEGP8ZIOqhxTvjGs",
            "Host": "www.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    
    }
    #设置cookie
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    headall = []
    # 将制定格式的headers信息添加好
    for key,value in headers.items():
        item = (key,value)
        headall.append(item)
    opener.addheaders = headall
    # 将opener安装为全局
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read()
    data = data.decode(encoding='utf-8')
#    print(data)
    return data
