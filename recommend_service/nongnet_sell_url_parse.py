# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 11:32:00 2018

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
import Tes
import iptest

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
    URL = "http://www.nongnet.com/default.aspx?PageID="+str(page)+"&classid=0&itype=2&prv=&city=&county="
    html = ''
    try:
        html = Tes.gethtml(URL)
    except:
        print('-------------------getParse0--Error--------------------------')
        time.sleep(0.1)
    return html
def getUrl(page):
    html = getParse0(page)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    urls = soup.find(id = 'ContentMain_lblList').find_all('ul')
    for i in range(len(urls)):
        u = urls[i].find_all('li')[0].find('a')['href']
        url = 'http://www.nongnet.com'+str(u)
        res.append(url)
    return res
def getRes(url):

    print('-------------------getRes--ing--------------------------')
    try:
        html =  Tes.gethtml(url)
    except:
        res = None
        return res
    print('-------------------getRes--Done--------------------------')
    print(url)
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    res['id'] = str(re.findall('\d+',url)[0])
    res['URL'] = url
    res['title'] = soup.find('h1',class_='h1class').get_text().replace(' ','').replace('\r\n','')
    divs = soup.find('div',class_='picandcontact').find_all('div',class_='xinxisxr')
    res['buyer_name'] = divs[1].get_text()
    res['phone'] = divs[2].get_text()
    res['location'] = divs[4].get_text()
    res['phone'] = divs[2].get_text()
    res['details'] = soup.find_all('div',class_='disxinxicontent')[1].get_text()
    start = soup.find_all('table')[1].find_all('div')[4].get_text()
    res['start_time'] = re.findall("：(.*) ",start)[0][:-8]
    title = res['title']
    print(title)
#    res['type'] = re.findall("[(.*)]",title)[0]
#    res['keywords'] = res['title'].get
#    trs= soup.find('div',class_='bg-white pad10 clearfix').find_all('tr')
#    res['count'] = trs[0].find_all('td')[1].get_text()
#    res['price'] = trs[1].find_all('td')[1].get_text()
#    time = soup.find('div',class_='font-gray').get_text()
#    res['start_time'] = re.findall('[^:]*',time)[0][5:]
#    res['end_time'] = soup.find_all('table')[1].find_all('td')[5].get_text()
#    res['details'] = soup.find(id = 'content').find_all('p')[0].get_text()
#    res['keywords'] = res['title']
#    res['location'] = soup.find_all('table')[1].find_all('td')[3].get_text() 
#    res['phone'] = sifany_util_math.find_phone(res['details'])

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
                
                obj['ID'] = str(res['id'])+str('-')+str(i+1)
                obj['URL'] = res['URL']
                obj['media'] = '农产品信息-买'
                obj['type'] = '买'
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = res['price']
                obj['count'] = res['count']
                obj['exceptation_location'] =''
#                obj['buyer_name'] = res['buyer_name']
                obj['keywords'] = analyse_type(res['keywords'],type_names)[i]
                obj['contact_location'] = res['location']
                obj['location'] = ''
                obj['start_time'] = res['start_time']
                obj['end_time'] = res['end_time']
                obj['detail'] = res['details']
                obj['lng'] = lngAndlat['lng']
                obj['lat'] = lngAndlat['lat']
                obj['phone']=sifany_util_math.find_phone(obj['detail']+obj['title'])
                print(obj)
#                sifany_util.insert_data(cursor,'corn_info',obj)
#                conn.commit()
                        
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
#                sifany_util.insert_data(cursor,'buyer',buyer)
#                conn.commit()
                print(buyer)
        else:
            obj['ID'] = res['id']
            obj['URL'] = res['URL']
            obj['media'] = '农产信息-买'
            obj['type'] = '买'
            obj['status'] = ''
            obj['title'] = res['title']
            obj['price'] = res['price']
            obj['count'] = res['count']
            obj['exceptation_location'] =''
            obj['buyer_name'] = res['buyer_name']
            obj['keywords'] = analyse_type(res['keywords'],type_names)
            obj['contact_location'] = res['location']
            obj['location'] = ''
            obj['start_time'] = res['start_time']
            obj['end_time'] = res['end_time']
            obj['detail'] = res['details']
            obj['lng'] = lngAndlat['lng']
            obj['lat'] = lngAndlat['lat']
            obj['phone']=sifany_util_math.find_phone(obj['detail']+obj['title'])
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
#            print(buyer)
            sifany_util.insert_data(cursor,'buyer',buyer)
            conn.commit()            
            
    except MyException as e:
        
        print(e.message)
        print('-----------------------------------Insert Error---------------------------')
        pass
    
    
            
def get_page_nums():
    url = "http://www.nongnet.com"
    html=sifany_util.getHtml(url)
    soup = BeautifulSoup(html,'html.parser')
    pages = soup.find('span',id='ContentMain_lblPage').get_text()
    page = re.findall('[^/]*',pages)[2][:-33]
    print(page)
    return page

def getData():
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data-test.json')
    pages=get_page_nums()
    print('pages',pages)
    for j in range(1,int(pages)):
        url = getUrl(j)
        print(url)
        for i in range(len(url)):
            res =getRes(url[i])
#            print(res)
            res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
            insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close() 
def get():
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data-test.json')
    res = getRes('http://www.zgncpw.com/buy/show-16437.html')
    res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
    insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    
if __name__=='__main__':
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data-test.json')
    url = getUrl(1)
    for i in url:
        res =getRes(i)
        print(res)
#        res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
#        insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close() 

    
    
    