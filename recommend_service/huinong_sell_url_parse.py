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
    URL = str(url)+'-0-0-0-0-'+str(page)+'/'
    try:
        html = sifany_util.getHtml(URL)
    except:
        print('-------------------getParse0--Error--------------------------')
        time.sleep(0.1)
    return html
def getUrl(page,url):
    html = getParse0(page,url)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    try:
        lis = soup.find(id = 'imgList').find_all('li')
        for i in range(len(lis)):
            url = lis[i].find('a',class_='img')['href']
            res.append(url)
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
    res['id'] = 'huinong-sell-'+str(re.findall('\d{7}',url)[0])
    res['URL'] = url
    res['title'] = soup.find('div',class_='tit clearfix').find('h1').get_text()
    loc = soup.find('div',class_='txt clearfix').get_text()
    try:
        res['location'] = loc[loc.find('发货地')+4:].replace('\n','')
    except:
        res['location'] = ''
    time = soup.find('div',class_='txt clearfix mt10').find('span').get_text()
    res['start_time'] = time[time.find('更新时间')+5:].replace('\n','')
    try:
        res['keywords'] = soup.find('div',class_='position').find_all('a')[1].get_text()
    except:
        res['keywords'] = None
    try:
        pri = soup.find('div',class_='price clearfix').find('span',class_='red fs24 mr5').get_text().replace('\n','')
        price = pri.replace(' ','')
        try:
            count = soup.find('div',class_='price clearfix').find('span',class_='mr15').get_text().replace('\n','')
        except:
            count = None
        res['price'] = str(price)+str(count)
    except:
        res['price'] = None    
    try:
        res['details'] = soup.find('div',class_='breed clearfix').get_text().replace('\n','')
    except:
        res['details'] = ''
    res['count'] = soup.find('div',class_='price clearfix').find_all('span',class_='mr5')[2].get_text()
#    print(res) 
    return res
class MyException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message 
def insertIntoDatabase(conn,res,lngAndlat,type_names):
    cursor=conn.cursor()
    try: 
        obj={}
        
        obj['media'] = '惠农网-卖'    
        obj['ID'] = res['id']
        obj['type']='卖'
        obj['URL'] = res['URL']
        obj['status'] = ''
        obj['title'] = res['title']
        obj['price'] = res['price']
        obj['count'] = res['count']
        obj['exceptation_location'] =''
        obj['buyer_name'] = ''
        obj['keywords'] = analyse_type(res['keywords']+res['title'],type_names)
        obj['contact_location'] = ''
        obj['location'] = res['location']
        obj['start_time'] = res['start_time']
        obj['end_time'] = ''
        obj['detail'] = res['details']
        obj['lng'] = lngAndlat['lng']
        obj['lat'] = lngAndlat['lat']
        obj['phone']=sifany_util_math.find_phone(obj['detail']+obj['title'])
#        print(obj)
        sifany_util.insert_data(cursor,'corn_info',obj)
                    
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

        if obj['type']=='卖':
            sifany_util.insert_data(cursor,'seller',buyer)
        else:
            sifany_util.insert_data(cursor,'buyer',buyer)
                    
        conn.commit()
            
    except MyException as e:
        
        print(e.message)
        print('-----------------------------------Insert Error---------------------------')
        pass
             
def get_page_nums(url):
    all_pages = []
    for i in range(len(url)):
        html=sifany_util.getHtml(url[i])
        soup = BeautifulSoup(html,'html.parser')
        a_all = soup.find('center').find_all('a')
        pages=int(a_all[5].get_text())
        all_pages.append(pages)    
    return all_pages
def get_product_url():
    html=sifany_util.getHtml('http://www.cnhnb.com/p/sgzw/')
    soup = BeautifulSoup(html,'html.parser')
    lis = soup.find(id = 'category_ul').find_all('li')
    product_url=[]
    for i in range(1,len(lis)):
        j =lis[i].find('a')['href']
        product_url.append(j[:-1])
    return product_url
def get_all_url():
    xianchenshu=10
    url = get_product_url()
    allpages_num = get_page_nums(url)#每个品种的总页数
    for j in allpages_num:# 遍历页码allpages_num[i]
        typess=sifany_util_math.trans_group(list(range(2,j)),xianchenshu)
        sifany_util.run_multi_process(getData,typess)

def getData(index):
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data-test.json')
    url = get_product_url()
    print('index',index)
    for i in range(0,len(url)):
        for j in index:
            page_url = getUrl(j,url[i])
            print('page_url',page_url)
            for k in page_url:
                res = getRes(k)
                print(res)
                res_lngAndlat=sifany_util_address.transPosition(conn,res['location'])
                insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close()

if __name__=='__main__':
    xianchenshu=10
    typess=sifany_util_math.trans_group(list(range(2,250)),xianchenshu)
    sifany_util.run_multi_process(getData,typess)
    
    