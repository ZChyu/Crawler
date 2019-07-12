# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:48:33 2018

@author: ReedGuo
"""
import sifany_util
import trade
conn0,cursor0,setting0=sifany_util.get_sql_conn("setting-data-test.json")
def get_seller_resources():
    sql='select * from seller where not ISNULL(product_id)'
    return sifany_util.get_dict_data_sql(cursor0,sql)
def get_buyer_resources():
    sql='select * from buyer where not ISNULL(product_id)'
    return sifany_util.get_dict_data_sql(cursor0,sql)
sellers= get_seller_resources()
buyers=get_buyer_resources()
def get_buyer_attr(buyer_id):
    sql='select * from corn_info where ID="'+buyer_id+'"'
    res=sifany_util.get_dict_data_sql(cursor0,sql)
    return res[0]
for seller in sellers:
    obj={}
    obj['product_id']=seller['product_id']
    obj['type']='0'
    obj['has_got']=0
    res=(trade.getBuyer(cursor0,seller))
   
    for resi in res:
        try:
            info=get_buyer_attr(resi['id'])
            print(str(info['phone']))
            if (str(info['phone']))!=str('None'):
                obj['score']=resi['score']
                obj['name']=resi['name']
                obj['price']=resi['price']
                obj['contact_name']=info['buyer_name']
                obj['product_res_id']=resi['product_id']
                obj['count']=resi['count']
                obj['address']=''
                obj['attr']=resi['attr']
                obj['phone']=info['phone']
                obj['url']=info['URL']
                obj['address']=info['location']
                sifany_util.insert_data(cursor0,'recommend_result_new',obj)
                conn0.commit()
            else:
                pass
        except:
            pass
print('seller----------------------------------------------------')
for buyer in buyers:
    obj={}
    obj['product_id']=buyer['product_id']
    obj['type']='1'
    obj['has_got']=0
    res=(trade.getSeller(cursor0,buyer))
    for resi in res:
        try:
            info=get_buyer_attr(resi['id'])
            print(str(info['phone']))
            if (str(info['phone']))!=str('None'):
                obj['score']=resi['score']
                obj['name']=resi['name']
                obj['price']=resi['price']
                obj['contact_name']=info['buyer_name']
                obj['product_res_id']=resi['product_id']
                obj['count']=resi['count']
                obj['address']=''
                obj['attr']=resi['attr']
                obj['phone']=info['phone']
                obj['url']=info['URL']
                obj['address']=info['location']
                sifany_util.insert_data(cursor0,'recommend_result_new',obj)
                conn0.commit()
            else:
                pass
        except:
            pass

conn0.close()
