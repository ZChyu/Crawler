# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:52:16 2018

@author: Zcy
"""
import sys
sys.path.append('D:\\workspace\\sifany_util\\')
import sifany_util
import sifany_util_address
import sifany_util_math
from bs4 import BeautifulSoup  
import time

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
    url = "http://www.cnhnb.com/purchase/0-0-0-0-0-"+str(page)+"/"
    try:
        html =sifany_util.getHtml(url,'utf-8')
    except:
        time.sleep(2)
    return html

def getUrl(page):
    html = getParse0(page)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    try:
        ul = soup.find('div',class_='wapper-w1190 clearfix').find('div',class_='pro-list mb_10').find_all('ul')
        li = ul[1].find_all('li')
        for i in range(50):
            res.append(li[i].find('a')['href'])
    except:
        res.append(None)
    return res


def getRes(url):
    html =sifany_util.getHtml(url,'utf-8')
    
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    res['id'] = url[url.find('caigou')+7:-1]
    res['URL'] = url
    ul = soup.find('div',class_= 'details').find('ul',class_='details-content')
    res['status'] = ul.find('p',class_='c1-name').find('span').get_text()
    res['title'] = ul.find('p',class_='c1-name').get_text()[ul.find('p',class_='c1-name').get_text().find('status')+1:-3]
    
    start_time = soup.find('div',class_='info-details').find('ul',class_='details-title').find('li',class_ = 'details-times').get_text()
    res['start_time'] = start_time[start_time.find('start_time')+6:]
    
    end_time = soup.find('div',class_='details-tips').find('p',class_='icon-time').get_text()
    res['end_time'] = end_time[end_time.find('end_time')+6:]
    
    res['keywords'] = res['title'][res['title'].find('[采购]')+5:]

    lis = ul.find_all('li')
    res['pin_zhong'] = lis[1].find('p').get_text()
    res['count'] = lis[2].find('p').get_text()
    price = lis[3].find('p').get_text()[+1:-1]
    
    res['exceptation_price'] = price.replace(' ','')
    res['exceptation_location'] = lis[4].find('p').get_text()
    res['buyer_name'] = soup.find('div',class_='details-contact').find('li',class_='contact-name').get_text()
    res['contact_location'] = soup.find('div',class_='details-contact').find('li',class_='contact-location').get_text()
    return res

def insertIntoDatabase(conn,cursor,res,lngAndlat,type_names):
    try:
        obj={}
        obj['ID'] = 'huinong-buy-'+res['id']
        obj['URL'] = res['URL']
        obj['media'] = '惠农-买'
        obj['status'] = res['status'] 
        obj['title'] = res['title']
        obj['price'] = res['exceptation_price']
        obj['count'] = res['count']
        obj['location']=res['exceptation_location'] 
        obj['exceptation_location'] = res['exceptation_location'] 
        obj['buyer_name'] = res['buyer_name']
        obj['keywords'] = analyse_type(res['keywords']+res['title'],type_names)
        obj['contact_location'] = res['contact_location']
        obj['start_time'] = res['start_time']
        obj['end_time'] = res['end_time']
        obj['lng'] = lngAndlat['lng']
        obj['lat'] = lngAndlat['lat']
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
        print(buyer['price'])    
        sifany_util.insert_data(cursor,'buyer',buyer)
        conn.commit()
    except:
        pass
def getData(indexs):
    sifany_util.create_ssl()
    conn,cursor,setting=sifany_util.get_sql_conn("setting-data-test.json")
    type_names=get_product_types()
    for i in indexs:
        url = getUrl(i)
        print('indexs:',indexs)
        print('url:',i)
        for j in url:
            res = getRes(j)
            print(res['contact_location'])
            res_lngAndlat=sifany_util_address.transPosition(conn,res['contact_location'])
            insertIntoDatabase(conn,cursor,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close()
if __name__=='__main__':
    xianchenshu=10
    typess=sifany_util_math.trans_group(list(range(1,200)),xianchenshu)
    sifany_util.run_multi_process(getData,typess)
   
    