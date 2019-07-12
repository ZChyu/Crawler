# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 17:06:41 2018

@author: Zcy
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:50:39 2018

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
def getParse0(page,url):
    print('-------------------getParse0--ing--------------------------')
    URL = str(url)+'/p_'+str(page)+'.html'
    print(URL)
    try:
        html = Tes.gethtml(URL)
    except:
        print('-------------------getParse0--Error--------------------------')
        time.sleep(5)
    return html
def getUrl(page,url):
    html = getParse0(page,url)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    try:
        lis = soup.find(id = 'content').find('ul',class_='main').find_all('li')
        for i in range(len(lis)):
            url = lis[i].find('a',class_='img')['href']
            print(url)
            res.append(url)
    except:
    
        res.append(None)
    print(res)
    return res
def getRes(url):

    print('-------------------getRes--ing--------------------------')
    try:
        html =  Tes.gethtml(url)
        time.sleep(5)
    except:
        res = None
        return res
    print('-------------------getRes--Done--------------------------')
    
    print(url)
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    res['id'] = '10000-sell-'+str(re.findall('cn/(.*)',url)[0])[:-5]
    res['URL'] = url
    try:
        res['title'] = soup.find('div',class_='head_main').find('h1').get_text()
    except:
        res['title'] = ''
#    print(soup.find('span',class_='o showprice').get_text())
    try:
        res['price'] = soup.find('div',class_='info').find('p',class_='price').find('span',class_='o showprice').get_text().replace(' ','').replace('\r\n\t','')
    except:
        res['price'] =''
    stime= soup.find('p',class_='time').get_text()
    res['start_time'] = re.findall('发布时间：(.*)',stime)[0]
    name = soup.find('p',class_='author').get_text()
    res['buyer_name']= re.findall('联系人：(.*)',name)[0].replace(' ','')
    location = soup.find('p',class_='area').get_text()
    res['contact_location'] = re.findall('地址：(.*)',location)[0]
    res['phone'] = soup.find('p',class_='phone').find('span',class_='r').get_text()
    res['details'] = soup.find('div',class_='details').find('p').get_text()
    res['keywords'] =res['title']+res['details']
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
        
                obj['media'] = '万农网-卖'    
                obj['ID'] = str(res['id'])+str('-')+str(i)
                obj['type']='卖'
                obj['URL'] = res['URL']
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = res['price']
                obj['count'] = None
                obj['exceptation_location'] =''
                obj['buyer_name'] = res['buyer_name']
                obj['keywords'] = analyse_type(res['details']+res['title'],type_names)[i]
                obj['contact_location'] = ''
                obj['location'] = res['contact_location']
                obj['start_time'] = res['start_time']
                obj['end_time'] = ''
                obj['detail'] = res['details']
                obj['lng'] = lngAndlat['lng']
                obj['lat'] = lngAndlat['lat']
                obj['phone']=res['phone']
                print(obj)
                sifany_util.insert_data(cursor,'corn_info',obj)
                            
                buyer={}
                buyer['id']=obj['ID'] 
                buyer['name']=obj['keywords']
                buyer['price']=sifany_util_math.trans_price_weight(obj['price'])
        
                buyer['count']=-1
                buyer['unit']='公斤'
                buyer['lat']=obj['lat']
                buyer['lon']=obj['lng']
                buyer['attr']=str(sifany_util_math.fetch_words(obj['title']+obj['detail']))
                print(buyer)
        
        
                sifany_util.insert_data(cursor,'seller',buyer)

        else:
                obj['media'] = '万农网-卖'    
                obj['ID'] = res['id']
                obj['type']='卖'
                obj['URL'] = res['URL']
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = res['price']
                obj['count'] = None
                obj['exceptation_location'] =''
                obj['buyer_name'] = res['buyer_name']
                obj['keywords'] = analyse_type(res['details']+res['title'],type_names)[0]
                obj['contact_location'] = ''
                obj['location'] = res['contact_location']
                obj['start_time'] = res['start_time']
                obj['end_time'] = ''
                obj['detail'] = res['details']
                obj['lng'] = lngAndlat['lng']
                obj['lat'] = lngAndlat['lat']
                obj['phone']=res['phone']
                print(obj)
                sifany_util.insert_data(cursor,'corn_info',obj)
                            
                buyer={}
                buyer['id']=obj['ID'] 
                buyer['name']=obj['keywords']
                buyer['price']=sifany_util_math.trans_price_weight(obj['price'])
        
                buyer['count']=-1
                buyer['unit']='公斤'
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
              

def get_product_url():
    html= Tes.gethtml('http://10000n.cn/')
    soup = BeautifulSoup(html,'html.parser')
    product_url=[]
    divs = soup.find(id='content').find_all('div')
    for i in range(2,3):
        print(i)
        lis = divs[i].find_all('li')
        
        for i in range(len(lis)):
            j =lis[i].find('a')['href']
            product_url.append(j)
    print(len(product_url))
    return product_url

def getData():
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data.json')
    urls = get_product_url()
    i=0
    for g in range(len(urls)):
        i=i+1
        print(urls[g])
        for j in range(all_pages[i-1]):
            print(j+1)
            page_url = getUrl(j,urls[g])
            print('page_url',page_url)
            for k in page_url:
                res = getRes(k)
                print(res)
                try:
                    res_lngAndlat=sifany_util_address.transPosition(conn,res['contact_location'])
                    insertIntoDatabase(conn,res,res_lngAndlat,type_names)
                except:
                    pass
    conn.commit()
    conn.close()
all_pages=[12,3,2,1,1,2,1,3,1,1]
#由于页数格式不一致，只能人工获得，还要修改get_product_url（）方法，爬取不同类别
if __name__=='__main__':
    getData()

    