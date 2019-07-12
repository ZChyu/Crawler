# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:48:30 2018

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
    URL = "https://www.nyxdt.net/buy/?page="+str(page)
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
    try:
        trs = soup.find('div',class_='m_gy_694 f_l').find('table').find_all('tr')
        for j in (0,16,32):
            td1 = trs[j].find_all('td')
            for i in (0,4,8,12,16):
                res.append(td1[i].find('td',class_='thumb').find('a')['href'])
    except:
        res.append(None)
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
    res['id'] = 'nongchan-buy-'+str(re.findall('\d+',url)[0])
    res['URL'] = url
    res['title'] = soup.find('div',class_='left_box').find('h1').get_text()
    trs = soup.find('div',class_='left_box').find_all('table')[3].find_all('tr')
    res['count'] = trs[0].find_all('td')[1].get_text().replace('\xa0','')
    res['price'] = str(trs[1].find_all('td')[1].get_text())
    try:
        res['location'] = trs[4].find_all('td')[1].get_text()
    except:
        res['location']= ' '
    res['keywords'] = res['title']
    res['end_time'] = trs[5].find_all('td')[1].get_text()
    res['start_time'] = trs[6].find_all('td')[1].get_text()
    try:
        name = soup.find(id = 'contact').find('ul').find_all('li')[2].get_text().replace('\n','')
        name1 = re.findall("[^(]*",str(name))[0][3:]
        if len(name1)<4:
            res['buyer_name'] = name1
        else:
            name = soup.find(id = 'contact').find('ul').find_all('li')[3].get_text().replace('\n','')
            name1 = re.findall("[^(]*",str(name))[0][3:]            
            res['buyer_name'] = name1
    except:
        pass
    print(res['buyer_name'])
    res['details'] = soup.find('div',class_='content c_b').get_text().replace('\xa0','') 

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
                obj['media'] = '农产信息-买'
                obj['type'] = '买'
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = res['price']
                obj['count'] = res['count']
                obj['exceptation_location'] =''
                obj['buyer_name'] = res['buyer_name']
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
    url = "https://www.nyxdt.net/buy/"
    html=sifany_util.getHtml(url)
    soup = BeautifulSoup(html,'html.parser')
    pages = soup.find('div',class_='pages').find('cite').get_text()[6:-1]
    return pages

def getData():
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data.json')
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
if __name__=='__main__':
    getData()

    
    
    