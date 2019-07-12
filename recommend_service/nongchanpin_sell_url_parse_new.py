# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:42:18 2018

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
    URL = "http://www.zgncpw.com/sell/?page="+str(page)
    print(URL)
    html=''
    try:
        html = sifany_util.getHtml(URL)
    except:
        print('-------------------getParse0--Error--------------------------')
        time.sleep(0.1)
    return html
def getUrl(page):
    html = getParse0(page)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    try:
        lis = soup.find('ul',class_='li-list-informaition').find_all('li')
        for i in range(len(lis)):
            url = lis[i].find('a',target='_blank')['href']
            res.append(url)
    except:
        res.append(None)
    return res
def getRes(url):
    print(url)
    print('-------------------getRes--ing--------------------------')
    try:
        html =  sifany_util.getHtml(url)
    except:
        res = None
        return res
    print('-------------------getRes--Done--------------------------')
    print(url)
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    res['id'] = 'nongchanpin-sell-'+str(re.findall('\d+',url)[0])
    res['URL'] = url
    try:
        key = soup.find('div',class_='fxl pos-text').find_all('a')[3].get_text()
        key2 = soup.find('div',class_='fxl pos-text').find_all('a')[4].get_text()
        res['title'] = str(soup.find('div',class_='fxr font clearfix').find('h1').get_text())+str(key)+str(key2)
    except:
        res['title'] = str(soup.find('div',class_='fxr font clearfix').find('h1').get_text())
    lis = soup.find('ul',class_='two l-big line-height-36 clearfix').find_all('li')
    price= lis[0].get_text()
    res['price'] = price.split('：')[1:][0]
    count= lis[2].get_text()
    res['count'] = count.split('：')[1:][0]
    try:
        location= lis[4].get_text()
        res['location'] = location.split('：')[1:][0]
    except:
        res['location'] =''
    end_time = lis[5].get_text()
    res['end_time'] = end_time.split('：')[1:][0]
    start_time = lis[6].get_text()
    res['start_time'] = start_time.split('：')[1:][0]
    res['details'] = soup.find('div',class_='content c_b').get_text().replace('\n','')
    res['phone']=str(sifany_util_math.find_phone(res['details'])).replace(' ','')
    res['keywords'] = res['title']
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
                obj['media'] = '农产品信息-卖'
                obj['type'] = '卖'
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = res['price']
                obj['count'] = res['count']
                obj['exceptation_location'] =''
                obj['buyer_name'] = ''
                obj['keywords'] = analyse_type(res['keywords'],type_names)[i]
                obj['contact_location'] = res['location']
                obj['location'] = ''
                obj['start_time'] = res['start_time']
                obj['end_time'] = res['end_time']
                obj['detail'] = res['details']
                obj['lng'] = lngAndlat['lng']
                obj['lat'] = lngAndlat['lat']
                obj['phone']=str(sifany_util_math.find_phone(obj['detail'])).replace(' ','')
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
                buyer['attr']=str(sifany_util_math.fetch_words(obj['title']+obj['detail']))
                sifany_util.insert_data(cursor,'seller',buyer)
                conn.commit()
                print(buyer)
        else:
            obj['ID'] = res['id']
            obj['URL'] = res['URL']
            obj['media'] = '农产品信息-卖'
            obj['type'] = '卖'
            obj['status'] = ''
            obj['title'] = res['title']
            obj['price'] = res['price']
            obj['count'] = res['count']
            obj['exceptation_location'] =''
            obj['buyer_name'] = ''
            obj['keywords'] = analyse_type(res['keywords'],type_names)
            obj['contact_location'] = res['location']
            obj['location'] = ''
            obj['start_time'] = res['start_time']
            obj['end_time'] = res['end_time']
            obj['detail'] = res['details']
            obj['lng'] = lngAndlat['lng']
            obj['lat'] = lngAndlat['lat']
            obj['phone']=str(sifany_util_math.find_phone(obj['detail'])).replace(' ','')
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
            buyer['attr']=str(sifany_util_math.fetch_words(obj['title']+obj['detail']))
            print(buyer)
            sifany_util.insert_data(cursor,'seller',buyer)
            conn.commit()            
            
    except MyException as e:
        
        print(e.message)
        print('-----------------------------------Insert Error---------------------------')
        pass
             
def get_page_nums():
    html=sifany_util.getHtml("http://www.zgncpw.com/sell/")
    soup = BeautifulSoup(html,'html.parser')
    a_all = soup.find('div',class_='pages').find('cite').get_text()
    pages = re.findall('[^/]*',a_all)[2][:-1]
    print(pages)
    return pages
def getData(index):
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data.json')
    for i in index:
        urls = getUrl(i)
        for url in urls:
            res = getRes(url)
            print(res)
            try:
                res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
                insertIntoDatabase(conn,res,res_lngAndlat,type_names)
            except:
                pass
    conn.commit()
    conn.close()
    
if __name__=='__main__':
    xianchenshu=10
    pages = get_page_nums()
    typess=sifany_util_math.trans_group(list(range(1,int(pages))),xianchenshu)
    sifany_util.run_multi_process(getData,typess)
    
    
    