# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:26:59 2018

@author: Zcy
"""
import sys
sys.path.append('D:\\workspace\\sifany_util\\')
import sifany_util
import sifany_util_address
import sifany_util_math
from bs4 import BeautifulSoup  
import time
import re


def get_product_types():
    types_f=open("product_types.txt",'r')
    types=types_f.read()
    types_f.close()
    types=types.split('\n')
    return types
def analyse_type(title,types):
    res=[]
    for typei in types:
        if title.find(typei)>-1:
            res.append(typei)
    return res
def getParse0(page):
    print('-------------------getParse0--ing--------------------------')
#    URL = "https://www.nyxdt.net/buy/?page="+str(page)
    URL = "http://www.eee.cn/search.jsp?province=370000&city=370200&district=&typeflag=0&type=2&swType=0&zhuanti=0&key=&strFenyeFlag=&strListCount=43826&maxPage=1461&repl="+str(page)
    print(URL)
    html = ''
    try:
        html = sifany_util.getHtml(URL)
        print(html)
    except:
        print('-------------------getParse0--Error--------------------------')
        time.sleep(0.1)
    return html
def getUrl(page):
    html = getParse0(page)
#    print(html)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    divs = soup.find_all('div')
#        href = divs.find('a')['href']
#        url = "http://www.eee.cn/"+str(href)
#        res.append(url)
    print(divs)
    return res
def getRes(url):

    print('-------------------getRes--ing--------------------------')
    html =  sifany_util.getHtml(url)
    print(html)
    try:
        html =  sifany_util.getHtml(url)
        print(html)
    except:
        res = None
        return res
    print('-------------------getRes--Done--------------------------')
    print(url)
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    res['id'] = 'eee-buy-'+str(re.findall('id=(.*)',url)[0])
    res['URL'] = url
  
    res['type'] =  soup.find('td',class_='heise_mx jiacu font16').get_text().replace('\r\n','')[:3].replace(' ','')
    res['title'] = soup.find('td',class_='heise_mx jiacu font16').get_text().replace('\r\n','')[3:].replace(' ','')
    res['buyer_name'] = soup.find('span',class_='jiacu').get_text().replace('\n','')
    location = soup.find('td',class_='heise_mx font14').get_text()
    res['location'] = re.findall('：\xa0(.*)',location)[0]
    phone = soup.find('span',class_='huise_mx jiacu').find('img')['src']
    res['phone'] = re.findall('str=(.*)',phone)[0]
    start = soup.find_all('td',class_='huise_mx')[0].get_text()
    res['start_time'] = re.findall('发布时间：(.*)',start)[0]
    end = soup.find_all('td',class_='huise_mx')[1].get_text()
    res['end_time'] = re.findall('有效期至：(.*)',end)[0]
    res['keywords'] = res['title']
    details = soup.find(id = 'enongDetail')
    print(res)
    return res
class MyException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message 
def insertIntoDatabase(conn,res,lngAndlat,type_names):
    cursor=conn.cursor()
    try:
        
        obj={}
        if len(analyse_type(res['keywords'],type_names))>1:
            for i in range(len(analyse_type(res['keywords'],type_names))):
                
                obj['ID'] = str(res['id'])+str('-')+str(i)
                obj['URL'] = res['URL']
                obj['media'] = '三农网-买'
                obj['type'] = '买'
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = ''
                obj['count'] = ''
                obj['exceptation_location'] =''
                obj['buyer_name'] = res['buyer_name']
                obj['keywords'] = analyse_type(res['keywords'],type_names)[i]
                obj['contact_location'] = res['location']
                obj['location'] = ''
                obj['start_time'] = res['start_time']
                obj['end_time'] = res['end_time']
                obj['detail'] = res['title']
                obj['lng'] = lngAndlat['lng']
                obj['lat'] = lngAndlat['lat']
                obj['phone']=res['phone']
                print(obj)
                sifany_util.insert_data(cursor,'corn_info',obj)
                conn.commit()
                        
                buyer={}
                buyer['id']=obj['ID'] 
                buyer['name']=obj['keywords']
                buyer['price']=sifany_util_math.trans_price_weight(obj['price'])
                count=sifany_util_math.trans_danwei_weight(obj['count'])
                buyer['count']=count['num']
                buyer['unit']=count['unit']
                buyer['lat']=obj['lat']
                buyer['lon']=obj['lng']
                buyer['attr']=str(sifany_util_math.fetch_words(obj['title']))
                sifany_util.insert_data(cursor,'buyer',buyer)
                conn.commit()
                print(buyer)
        else:
            obj['ID'] = res['id']
            obj['URL'] = res['URL']
            obj['media'] = '三农网-买'
            obj['type'] = '买'
            obj['status'] = ''
            obj['title'] = res['title']
            obj['price'] = ''
            obj['count'] = ''
            obj['exceptation_location'] =''
            obj['buyer_name'] = res['buyer_name']
            obj['keywords'] = analyse_type(res['keywords'],type_names)
            obj['contact_location'] = res['location']
            obj['location'] = ''
            obj['start_time'] = res['start_time']
            obj['end_time'] = res['end_time']
            obj['detail'] = res['title']
            obj['lng'] = lngAndlat['lng']
            obj['lat'] = lngAndlat['lat']
            obj['phone']=res['phone']
            print(obj)
            sifany_util.insert_data(cursor,'corn_info',obj)
            conn.commit()
                        
            buyer={}
            buyer['id']=obj['ID'] 
            buyer['name']=obj['keywords']
            buyer['price']=sifany_util_math.trans_price_weight(obj['price'])
            count=sifany_util_math.trans_danwei_weight(str(obj['count']))
            buyer['count']=count['num']
            buyer['unit']=count['unit']
            buyer['lat']=obj['lat']
            buyer['lon']=obj['lng']
            buyer['attr']=str(sifany_util_math.fetch_words(obj['title']))
            print(buyer)
            sifany_util.insert_data(cursor,'buyer',buyer)
            conn.commit()            
            
    except MyException as e:
        
        print(e.message)
        print('-----------------------------------Insert Error---------------------------')
        pass

def getData(index):
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data.json')
    for j in index:
        url = getUrl(j)
        print(url)
        for i in range(len(url)):
            res =getRes(url[i])
#            print(res)
            res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
            insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close() 
if __name__=='__main__':
#    xianchenshu=10
#    typess=sifany_util_math.trans_group(list(range(2,134)),xianchenshu)
#    sifany_util.run_multi_process(getData,typess)
#    getUrl(2)
#    getRes('http://www.eee.cn/search.jsp?province=370000&city=370200&district=&typeflag=&type=0&swType=0&zhuanti=0&key=&strFenyeFlag=1&strListCount=48571&maxPage=1620&repl=227')
    sifany_util.getHtml('http://www.eee.cn/search.jsp?province=370000&city=370200&district=&typeflag=&type=0&swType=0&zhuanti=0&key=&strFenyeFlag=1&strListCount=48571&maxPage=1620&repl=37')
    
    
    