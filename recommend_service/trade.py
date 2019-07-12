# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 09:45:18 2018

@author: summer
"""
import sifany_util
import numpy as np
import re
def checkFalse(price1,price2):
    print(price1,' ',price2 )
    if price1==None or price2==None or price1==-1 or price2==-1:
        return True
    return False
def cal_price_score_buyer(buyer_price,seller_price):
    if checkFalse(buyer_price,seller_price):return 0
    
    p = float(buyer_price)-float(seller_price)
    res = 1/(1+float(np.exp(-p)))  
    return res
def cal_count_score_buyer(buyer_count,seller_count):
    if checkFalse(buyer_count,seller_count):return 0
    c = float(buyer_count) - float(seller_count)
    c=c/5000
    res = 1/(1+float(np.exp(-c)))  
    return res
def cal_position_score(buyer_lat,buyer_lon,seller_lat,seller_lon,k1,k2):
    l = np.sqrt(np.square(buyer_lat-seller_lat)+np.square(buyer_lon-seller_lon))
    res = k1*(float(np.exp(k2*l)-1))
    res = 1/(1+float(np.exp(-res)))
    res=1-res
   
    return res
def cal_attr_score_buyer(buyer_attr,seller_attr):
    buyer_attr=eval(buyer_attr)  
    seller_attr=eval(seller_attr)
    seller_attr=set(seller_attr)
    score=0
    for attr in buyer_attr:
        if attr in seller_attr:
            score=score+1
    score=score/len(buyer_attr)
    res= int(score*100)/100
    print('res',res)
    return res
def cal_score_buyer(buyer_data,seller_data,k1,k2,w1,w2,w3,w4):
  
    score=w1*cal_price_score_buyer(buyer_data['price'],seller_data['price'])+\
        w2*cal_count_score_buyer(buyer_data['count'],seller_data['count'])+\
        w3*cal_position_score(buyer_data['lat'],buyer_data['lon'],seller_data['lat'],seller_data['lon'],k1,k2)+\
        w4*cal_attr_score_buyer(buyer_data['attr'],seller_data['attr'])
    return int(score*100)/100
    
def filter_buyer_data(buyer_datas,seller_data,k1,k2,w1,w2,w3,w4,n):
    score_list=[]
    for buyer_data in buyer_datas:
        buyer_data['score']=cal_score_buyer(buyer_data,seller_data,k1,k2,w1,w2,w3,w4)
        score_list.append(buyer_data)
    score_list.sort(key=lambda x:x['score'],reverse=True)
    
    return score_list[0:n]
def getBuyer(cursor,seller_data,lat_psi=25,lon_psi=25,k1=2,k2=0.01,w1=0.25,w2=0.25,w3=0.25,w4=0.25,n=30):
    buyer_data=sifany_util.get_dict_data_sql(cursor,"SELECT * FROM buyer where name='"+seller_data['name']
    +"' AND ABS(lat-"+str(seller_data['lat'])+")<"+str(lat_psi)
    +" AND ABS(lon-"+str(seller_data['lon'])+")<"+str(lon_psi))
    score_list =filter_buyer_data(buyer_data,seller_data,k1,k2,w1,w2,w3,w4,n)

    return getScore(cursor,score_list)
def cal_attr_score_seller(buyer_attr,seller_attr):    
    buyer_attr=eval(buyer_attr)  
    seller_attr=eval(seller_attr)
    buyer_attr=set(buyer_attr)
    score=0
    for attr in seller_attr:
        if attr in buyer_attr:
            score=score+1
    score=score/len(seller_attr)
    res= int(score*100)/100
    print('res',res)
    return res

def cal_price_score_seller(buyer_price,seller_price):
    if checkFalse(buyer_price,seller_price):return 0
    p = seller_price-buyer_price  
    res = 1/(1+float(np.exp(-p)))  
    return res

def cal_count_score_seller(buyer_count,seller_count):
    if checkFalse(buyer_count,seller_count):return 0
    c =  seller_count-buyer_count 
    c=c/5000
    res = 1/(1+float(np.exp(-c)))
    return res
def cal_score_seller(buyer_data,seller_data,k1,k2,w1,w2,w3,w4): 
    score=w1*cal_price_score_seller(buyer_data['price'],seller_data['price'])+\
        w2*cal_count_score_seller(buyer_data['count'],seller_data['count'])+\
        w3*cal_position_score(buyer_data['lat'],buyer_data['lon'],seller_data['lat'],seller_data['lon'],k1,k2)+\
        w4*cal_attr_score_seller(buyer_data['attr'],seller_data['attr'])
    return int(score*100)/100
    
def filter_seller_data(buyer_data,seller_datas,k1,k2,w1,w2,w3,w4,n):
    score_list=[]
    for seller_data in seller_datas:
        seller_data['score']=cal_score_seller(seller_data,buyer_data,
                           k1,k2,w1,w2,w3,w4)

        score_list.append(seller_data)
    score_list.sort(key=lambda x:x['score'],reverse=True)
    
    return score_list[0:n]

def getSeller(cursor,buyer_data,lat_psi=25,lon_psi=25,k1=2,k2=0.01,w1=0.25,w2=0.25,w3=0.25,w4=0.25,n=30):     
    seller_data=sifany_util.get_dict_data_sql(cursor,"SELECT * FROM seller where name='"+buyer_data['name']
    +"' AND ABS(lat-"+str(buyer_data['lat'])+")<"+str(lat_psi)
    +" AND ABS(lon-"+str(buyer_data['lon'])+")<"+str(lon_psi))
    
    score_list = filter_seller_data(buyer_data,seller_data,k1,k2,w1,w2,w3,w4,n)
    return getScore(cursor,score_list)

def getScore(cursor,score_list):
    
    score_lists = []
    try:
        for buyerdata in score_list:
            data = sifany_util.get_dict_data_sql(cursor,'select * from corn_info where id="'+buyerdata['id']+'"')
            if data[0]['phone']!=None:
                score = 1
            else:
                score = 0
                print('phone is null')
            if int(re.findall('\d{4}',data[0]['start_time'])[0].decode('utf-8'))>=2018:
                score1 = 1
            else:
                score1 = 0
            if data[0]['buyer_name']==None:
                score3=0
                print('name is null')
            else:
                score3=1
                
            s = buyerdata['score']+score+score1*2+score3
            buyerdata['score'] =float(1/(1+float(np.exp(-s))))
            score_lists.append(buyerdata)
        score_lists.sort(key=lambda x:x['score'],reverse=True)
    except:
        score_lists=score_list
    return score_lists
