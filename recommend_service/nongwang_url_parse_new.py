# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:50:39 2018

@author: Zcy
"""
from bs4 import BeautifulSoup  
import time
import sifany_util
import sifany_util_address
import sifany_util_math
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
    url = "http://hlj.nongwang.com/gongqiu/I-99-0-0-0-0-"+str(page)+".html"
    try:
        html = sifany_util.getHtml(url)
    except:
        print('-------------------getParse0--Error--------------------------')
        time.sleep(0.1)
    return html
def getUrl(page):
    html = getParse0(page)
    soup = BeautifulSoup(html,'html.parser') 
    res = []
    try:
        div_class = soup.find('div',class_='left_box').find_all('div',class_='list')
        for i in range(len(div_class)):
            url = div_class[i].find('a')['href']
            res.append(url)
    except:
        res.append(None)  
    return res
def getRes(url):
    print('-------------------getRes--ing--------------------------')
    html =  sifany_util.getHtml(url)    
    print('-------------------getRes--Done--------------------------')
    soup = BeautifulSoup(html,'html.parser')
    res ={}
    res['id'] = url[url.find('show')+5:-5]
    res['URL'] = url
    res['title'] = soup.find('div',class_='left_box').find('h1',class_='title_trade').get_text()
    trss = soup.find('div',class_='left_box').find('table').find_all('tr')
    trs = trss[1].find_all('tr')
    
    type_name= trs[3].find_all('td')[1].get_text()
    res['type'] = type_name.replace('\xa0','')
    key = trs[4].find_all('td')[1].get_text()
    res['keywords'] = key.replace('\xa0','')
    price = trs[7].find_all('td')[1].get_text()
    res['price'] = price.replace('\xa0','')
    count = trs[8].find_all('td')[1].get_text()
    res['count'] = count.replace('\xa0','')
    buyer_name = trs[9].find_all('td')[1].get_text()
    res['buyer_name'] = buyer_name.replace(' ','')
    #['phone'] = trs[10].find_all('td')[1].find('img')['src']
    res['end_time'] = trs[11].find_all('td')[1].get_text()
    res['start_time'] = trs[12].find_all('td')[1].get_text()
    detils = soup.find(id= 'content').get_text()
    res['detail'] = detils.replace('\xa0','')
    location = soup.find('div',class_='left_box').find('span',class_='f_green').get_text()
    res['contact_location'] = location.replace('-','')
    
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
                if res['type']=='供应':
                    obj['media'] = '农网-卖'    
                    obj['ID'] ='nongwang-sell-'+str(res['id'])+str('-')+str(i)
                    print(obj['ID'])
                    obj['type']='卖'
                else:
                    obj['media'] = '农网-买'    
                    obj['ID'] ='nongwang-buy-'+str(res['id'])+str('-')+str(i)
                    print(obj['ID'])
                    obj['type']='买'
                obj['URL'] = res['URL']
                obj['status'] = ''
                obj['title'] = res['title']
                obj['price'] = res['price']
                obj['count'] = res['count']
                obj['exceptation_location'] =''
                obj['buyer_name'] = res['buyer_name']
                obj['keywords'] = analyse_type(res['keywords'],type_names)[i]
                obj['contact_location'] = res['contact_location']
                obj['location'] = res['contact_location']
                obj['start_time'] = res['start_time']
                obj['end_time'] = res['end_time']
                obj['detail'] = res['detail']
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
                buyer['attr']=str(sifany_util_math.fetch_words(obj['title']+obj['detail']))
                
                if res['type']=='供应':
                    sifany_util.insert_data(cursor,'seller',buyer)
                else:
                    sifany_util.insert_data(cursor,'buyer',buyer)
                
                conn.commit()
        else:
                if res['type']=='供应':
                    obj['media'] = '农网-卖'    
                    obj['ID'] ='nongwang-sell-'+res['id']
                    obj['type']='卖'
                else:
                    obj['media'] = '农网-买'    
                    obj['ID'] ='nongwang-buy-'+res['id']
                    obj['type']='买'
                    obj['URL'] = res['URL']
                    obj['status'] = ''
                    obj['title'] = res['title']
                    obj['price'] = res['price']
                    obj['count'] = res['count']
                    obj['exceptation_location'] =''
                    obj['buyer_name'] = res['buyer_name']
                    obj['keywords'] = analyse_type(res['keywords'],type_names)
                    obj['contact_location'] = res['contact_location']
                    obj['location'] = res['contact_location']
                    obj['start_time'] = res['start_time']
                    obj['end_time'] = res['end_time']
                    obj['detail'] = res['detail']
                    obj['lng'] = lngAndlat['lng']
                    obj['lat'] = lngAndlat['lat']
                    obj['phone']=sifany_util_math.find_phone(obj['detail']+obj['title'])
                    print(obj)
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

                    if res['type']=='供应':
                        sifany_util.insert_data(cursor,'seller',buyer)
                    else:
                        sifany_util.insert_data(cursor,'buyer',buyer)
                    
                    conn.commit()
            
    except MyException as e:
        
        print(e.message)
        print('-----------------------------------Insert Error---------------------------')
        pass           
def run_a_proc(types):
    sifany_util.create_ssl()
    type_names=get_product_types()
    conn,cursor,_=sifany_util.get_sql_conn('setting-data-test.json')
    for typei in types:
        url = getUrl(typei)
        print('url:',typei)
        for j in url:     #每页的的url遍历
            res = getRes(j)
            res_lngAndlat=sifany_util_address.transPosition(conn,res['contact_location'])
            
            insertIntoDatabase(conn,res,res_lngAndlat,type_names)
    conn.commit()
    conn.close()
def get_page_nums():
    html=sifany_util.getHtml('http://hlj.nongwang.com/gongqiu/I-99-0-0-0-0.html')
    soup = BeautifulSoup(html,'html.parser')
    all_pages=int(re.findall('\d+',(soup.find('cite').get_text()))[1])
    return all_pages

if __name__=='__main__':
    
    proc_num=2
    all_pages=get_page_nums()
    typess=sifany_util_math.trans_group(list(range(1,all_pages+1)),proc_num)
    #run_a_proc([1])
    sifany_util.run_multi_process(run_a_proc,typess)
    
    