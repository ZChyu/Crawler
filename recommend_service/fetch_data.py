# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 10:55:28 2018

@author: ReedGuo
"""
import sys
sys.path.append('D:\\workspace\\sifany_util\\')
import urllib.request
import ssl
import pymysql
import json

import sifany_util





def getData(keywords):
    conn,cursor=get_sql_conn("setting-data.json")
    for i in range(50):
        data=[];
        for j in range(1,7):
            res=getParse(keywords,i,j)
            temp = getIDAndURL(res,keywords)
            data.extend(temp)
               
       
    conn.close()