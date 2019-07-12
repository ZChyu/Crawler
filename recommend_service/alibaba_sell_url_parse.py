# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 11:03:46 2018

@author: ReedGuo
"""
import sys
sys.path.append('D:\\workspace\\sifany_util\\')
import sifany_util
import sifany_util_address
import sifany_util_math
from multiprocessing import Pool
from bs4 import BeautifulSoup  
import urllib
import json
from jieba import analyse
def getParse(name,page,asy):
    url= "https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage="+str(page)+"&asyncreq="+str(asy)+"&keywords="+urllib.request.quote(name)
    html = sifany_util.getHtml(url)
    jsondata=json.loads(html)
    return jsondata
def insertIntoDatabase(cursor,res,lngAndlat,ID,keywords):
    try:
        obj={}
        obj['ID'] = 'alibaba-sell-'+ID
        obj['URL'] = res['URL']
        obj['title'] = res['title']
        obj['price'] = res['general_price']
        obj['count'] = res['amount']
        obj['phone'] = res['phone']
        obj['location'] = res['location'] 
        obj['URL'] = res['URL']
        obj['lng'] = lngAndlat['lng']
        obj['lat'] = lngAndlat['lat']
        obj['keywords'] = keywords
        obj['media'] = '阿里巴巴-卖'
        sifany_util.insert_data(cursor,'corn_info',obj)
        print('obj:',obj['price'])  
        
        seller={}
        seller['id']=obj['ID'] 
        seller['name']=keywords
        seller['price']=obj['price']
        try:
            count=sifany_util_math.trans_danwei_weight(obj['count'])
            seller['count']=count['num']
        except:
            seller['count']=None        
        print(seller['price'])
        seller['lat']=obj['lat']
        seller['lon']=obj['lng']
        seller['attr']=str(analyse.extract_tags(obj['title']))
        print('seller:',seller['price']) 
        sifany_util.insert_data(cursor,'seller',seller)
    except:
        pass         

def getIDAndURL(data,keywords):
    res = []
    if "data" in data.keys():
        data = data["data"]
    else:
        print("not has data key")
        print(data.keys())
        return 0
    if "content" in data.keys():
        data = data["content"]
    else:
        print("not has content key")
        print(data.keys())
        return 0
    if "offerResult" in data.keys():
        data = data["offerResult"]
    else:
        print("not has offerResult key")
        print(data.keys())
        return 0;
    for i in range(len(data)):
        if data[i]["title"].__contains__(keywords):
            res.append([data[i]["offerid"],data[i]["title"]])
    return res
def parseUrl(url):
    
    html = sifany_util.getHtml(url,'gbk')
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    pro = []
    res['URL'] = url
    try:
        res['title'] = soup.find(id = 'site_content_fluid').find('div',class_='mod-detail-title detail-static static-content').find('h1',class_='d-title').get_text()
    except:
        res['title']= None
    try:
        res['general_price']  = soup.find(id='mod-detail-price').find('span',class_='value').get_text()
    except:
        res['general_price'] = None
        
    try:
        count_trs = soup.find(id = 'site_content_fluid').find('div',class_='obj-content').find_all('tr')
        count_tds = count_trs[0].find_all('td')
        res['amount'] = count_tds[2].find('span').find('em',class_='value').get_text()
    except:
        res['amount'] = None
        
    try:    
        res['location'] = soup.find(id = 'doc').find('div',class_='obj-parcel').find('span',class_='delivery-addr').get_text()
    except:
        res['location'] = '不限'  
    try:
        p= soup.find(id = 'site_content').find('dl',class_='m-mobilephone')['data-no']
        res['phone'] = p.replace(' ','')
    except:
        res['phone'] = None
    property_trs=None
    try:
        property_trs = soup.find(id = 'mod-detail-attributes').find('div',class_='obj-content').find_all('tr')
    except:
        res['pro'] = str(tuple(pro))
        return res
    for i in range(5):
        try:
            tds = property_trs[i].find_all('td')
            pro.append(tds[0].get_text())
            pro.append(tds[1].get_text())
            pro.append(tds[2].get_text())
            pro.append(tds[3].get_text())
            pro.append(tds[4].get_text())
            pro.append(tds[5].get_text())
        except:
            pro.append(None)
    res['pro'] = str(tuple(pro))
        
    return res

def getData(keywords):
    conn,cursor,setting=sifany_util.get_sql_conn("setting-data-test.json")
    for i in range(50):
        for j in range(1,7):
            res=getParse(keywords,i,j)
            data_url = getIDAndURL(res,keywords)
            for data_urli in data_url:
                ID=str(data_urli[0])
                sql='select count(*) from corn_info where ID="'+'alibaba-sell-'+ID+'"'
                cursor.execute(sql)
                data=cursor.fetchall()
                if(data[0][0]>0):
                    continue
                try:
                    url="https://detail.1688.com/offer/"+str(data_urli[0])+".html"
                    print(url)
                    url_res=parseUrl(url)
                    print(url_res)
                    res_lngAndlat=sifany_util_address.transPosition(conn,url_res['location'])
                    
                    insertIntoDatabase(cursor,url_res,res_lngAndlat,data_urli[0],keywords)
                    conn.commit()
                except:
                    pass
       
    conn.close()
def get_product_types():
    types_f=open("product_types.txt",'r')
    types=types_f.read()
    types_f.close()
    types=types.split('\n')
    return types
def deal_list(types):
    for typei in types:
        getData(typei)

def refresh_url_datas():
    types=get_product_types()
#    deal_list(types)
    
    xianchenshu=10
    typess=sifany_util_math.trans_group(types,xianchenshu)
    p = Pool(xianchenshu+1)
    for types in typess:
        p.apply_async(deal_list, args=(types,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
   
if __name__=='__main__':        
    refresh_url_datas()