# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 17:46:33 2018

@author: Lidh
"""   
import sys
sys.path.append('D:\\workspace\\sifany_util\\')
import sifany_util
from jieba import analyse
import sifany_util_address
def fetch_datas_sql():
    conn,cursor,setting=sifany_util.get_sql_conn("setting-data-nonglv.json")
    nonlv_fetch_data_sql_f=open("nonlv_fetch_data.sql",'r')
    nonlv_fetch_data_sql=nonlv_fetch_data_sql_f.read()
    nonlv_fetch_data_sql_f.close()
    nonglv_data=sifany_util.get_dict_data_sql(cursor,nonlv_fetch_data_sql)
    conn.close()
    return nonglv_data
def get_product_types():
    types_f=open("product_types.txt",'r')
    types=types_f.read()
    types_f.close()
    types=types.split('\n')
    return types
def analyse_type(title,types):
    for typei in types:
        if title.find(typei)>-1:
            return typei
    return None
def fetch_datas():
    sql_data=fetch_datas_sql()
    conn,cursor,setting=sifany_util.get_sql_conn("setting-data.json")
    types=get_product_types()
    
    for data in sql_data:
        md5_key=sifany_util.md5(data['id']+str(data['modifyDate']))
        print('md5',md5_key)
        md5_result=sifany_util.get_dict_data_sql(cursor,'select * from nonglv_has_fetch where md5_v="'+md5_key+'"')
        if len(md5_result)==0:
            info={}
            info['ID']=data['id']
            info['URL']=data['url']
            
            info['title']=data['title']
            
            info['phone']=data['phone']
            
            info['location']=data['appregion_name']
            sifany_util.insert_data(cursor,'corn_info',info)
            conn.commit()
            if data['state']==0:
                seller_result=sifany_util.get_dict_data_sql(cursor,'select * from seller where product_id="'+data['id']+'"')
                seller={}
                seller['name']=analyse_type(data['title'],types)
                if seller['name']==None:
                    continue
                seller['id']=data['id']
                seller['price']=data['price']
                seller['count']=data['count']
                seller['attr']=str(analyse.extract_tags(data['Description']))
                seller['product_id']=data['id']
                lngAndlat=sifany_util_address.transPosition(conn,data['appregion_name'])
                seller['lon'] = lngAndlat['lng']
                seller['lat'] = lngAndlat['lat']
                seller['product_id']=data['id']
                seller['product_update_time']=data['modifyDate']
                if len(seller_result)==0:
                    sifany_util.insert_data(cursor,'seller',seller)
                else:
                    sifany_util.update_data(cursor,'seller',seller,'id')
                    
            else:
                seller_result=sifany_util.get_dict_data_sql(cursor,'select * from buyer where product_id="'+data['id']+'"')
                seller={}
                seller['name']=analyse_type(data['title'],types)
                if seller['name']==None:
                    continue
                seller['id']=data['id']
                seller['price']=data['price']
                seller['count']=data['count']
                seller['attr']=str(analyse.extract_tags(data['Description']))
                seller['product_id']=data['id']
                lngAndlat=sifany_util_address.transPosition(conn,data['appregion_name'])
                seller['lon'] = lngAndlat['lng']
                seller['lat'] = lngAndlat['lat']
                seller['product_id']=data['id']
                seller['product_update_time']=data['modifyDate']
                if len(seller_result)==0:
                    sifany_util.insert_data(cursor,'buyer',seller)
                else:
                    sifany_util.update_data(cursor,'buyer',seller,'id')
            nonglv_has_fetch={}
            nonglv_has_fetch['md5_v']=md5_key
            nonglv_has_fetch['id']=data['id']
            sifany_util.insert_data(cursor,'nonglv_has_fetch',nonglv_has_fetch)
            
    conn.commit()
    conn.close()
if __name__=='__main__':
    fetch_datas()