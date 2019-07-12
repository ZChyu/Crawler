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
    URL = "http://www.zgncpw.com/buy/?page="+str(page)
    html = ''
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
    trs = soup.find('div',class_='con-width-1200 sub clearfix').find('table').find_all('tr')
    for i in range(1,len(trs)):
        res.append(trs[i].find('a')['href'])
    return res
def getRes(url):

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
    res['id'] = 'nongchanpin-buy-'+str(re.findall('\d+',url)[0])
    res['URL'] = url
    res['title'] = soup.find(id='title').get_text()
    res['keywords'] = res['title']
    trs= soup.find('div',class_='bg-white pad10 clearfix').find_all('tr')
    res['count'] = trs[0].find_all('td')[1].get_text()
    res['price'] = trs[1].find_all('td')[1].get_text()
    time = soup.find('div',class_='font-gray').get_text()
    res['start_time'] = re.findall('[^:]*',time)[0][5:]
    res['end_time'] = soup.find_all('table')[1].find_all('td')[5].get_text()
    try:
        res['details'] = soup.find(id = 'content').find_all('p')[0].get_text()
    except:
        res['details'] = None
    res['keywords'] = str(res['title'])+str(res['details'])
    try:
        res['location'] = soup.find(id= 'content').get_text()
#        res['location'] = soup.find_all('table')[1].find_all('td')[3].get_text() 
    except:
        res['location'] ='不限'
    res['phone'] = sifany_util_math.find_phone(res['details'])

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
                obj['media'] = '农产品信息-买'
                obj['type'] = '买'
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
                obj['phone']=sifany_util_math.find_phone(obj['detail']+obj['title'])
                print(obj)
                sifany_util.insert_data(cursor,'corn_info',obj)
                conn.commit()
                        
                buyer={}
                buyer['id']=obj['ID'] 
                buyer['name']=analyse_type(res['keywords'],type_names)[i]
                buyer['price']=sifany_util_math.trans_price_weight(obj['price'])
                count=sifany_util_math.trans_danwei_weight(obj['count'])
                buyer['count']=count['num']
                buyer['unit']=count['unit']
                buyer['lat']=obj['lat']
                buyer['lon']=obj['lng']
                buyer['attr']=str(sifany_util_math.fetch_words(obj['title']+obj['detail']))
                sifany_util.insert_data(cursor,'buyer',buyer)
                conn.commit()
                print(buyer)
        else:
            obj['ID'] = res['id']
            obj['URL'] = res['URL']
            obj['media'] = '农产品信息-买'
            obj['type'] = '买'
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
            obj['phone']=sifany_util_math.find_phone(obj['detail']+obj['title'])
            print(obj)
            sifany_util.insert_data(cursor,'corn_info',obj)
            conn.commit()
                        
            buyer={}
            buyer['id']=obj['ID'] 
            buyer['name']=analyse_type(res['keywords'],type_names)
            buyer['price']=sifany_util_math.trans_price_weight(obj['price'])
            count=sifany_util_math.trans_danwei_weight(str(obj['count']))
            buyer['count']=count['num']
            buyer['unit']=count['unit']
            buyer['lat']=obj['lat']
            buyer['lon']=obj['lng']
            buyer['attr']=str(sifany_util_math.fetch_words(obj['title']+obj['detail']))
            print(buyer)
            sifany_util.insert_data(cursor,'buyer',buyer)
            conn.commit()            
            
    except MyException as e:
        
        print(e.message)
        print('-----------------------------------Insert Error---------------------------')
        pass
    
def getName(page):
    html = getParse0(page)
    soup = BeautifulSoup(html,'html.parser') 
    name = []
    trs = soup.find('div',class_='con-width-1200 sub clearfix').find('table').find_all('tr')
    for i in range(1,len(trs)):
        name.append(trs[i].find_all('td')[3].get_text().replace('\r\n',''))
        
    return name  
            
def get_page_nums():
    url = "http://www.zgncpw.com/buy/"
    html=sifany_util.getHtml(url)
    soup = BeautifulSoup(html,'html.parser')
    pages = soup.find('div',class_='pages').find('cite').get_text()[7:-1]
    return pages

def getData(index):
    sifany_util.create_ssl()
    type_names=get_product_types()
#    pages=get_page_nums()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data.json')

    for j in index:
        urls = getUrl(j)
        print(urls)
        for url in urls:
            print(url)
            try:
                res =getRes(url)
                print(res)
                print(res['location'])
                res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
                insertIntoDatabase(conn,res,res_lngAndlat,type_names)
            except:
                pass
    conn.commit()
    conn.close() 
def get():
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data.json')
    res = getRes('http://www.zgncpw.com/buy/show-16417.html')
    res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
    insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close() 
if __name__=='__main__':
    xianchenshu=10
    pages=get_page_nums()
    typess=sifany_util_math.trans_group(list(range(1,int(pages))),xianchenshu)
    sifany_util.run_multi_process(getData,typess)
    
    
    