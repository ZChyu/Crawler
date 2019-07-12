# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 13:54:49 2018

@author: Gao Bangpeng

@Email: bangpenggao@163.com
"""
import sys
sys.path.append('D:\\workspace\\sifany_util\\')
import json
import requests
from flask import Flask,render_template,request,Response
import recommend
import sifany_util
conn0,cursor0,setting0=sifany_util.get_sql_conn("setting-data.json")
app=Flask(__name__)


def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/",methods=["POST"])
def test():
    if request.method=="POST":
        data = request.form.to_dict()
        # print(data)
        content = str(data)
        resp = Response_headers(content)
        recommend.main()
        sql='select * from seller where not ISNULL(product_id)'
        res = sifany_util.get_dict_data_sql(cursor0,sql)
        if len(res)==0:
        	content = json.dumps({"FILED":"FILED"})  
        	resp = Response_headers(content)  
        	return resp 
        else:
        	content = json.dumps({"SUCCESS":"SUCCESS"})  
        	resp = Response_headers(content)  
        	return resp
    else:
        content = json.dumps({"error_code":"1001"})  
        resp = Response_headers(content)  
        return resp 

#test post method
@app.route("/postdata")
def postData():
    res=requests.post(url="http://127.0.0.1:5000",data={"username":123,"password":456})
    print(res)
    resp = Response_headers(res)
    return resp

@app.errorhandler(403)
def page_not_found(error):
    content = json.dumps({"error_code": "403"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(404)
def page_not_found(error):
    content = json.dumps({"error_code": "404"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(400)
def page_not_found(error):
    content = json.dumps({"error_code": "400"})
    # resp = Response(content)  
    # resp.headers['Access-Control-Allow-Origin'] = '*'  
    resp = Response_headers(content)
    return resp
    # return "error_code:400"  

@app.errorhandler(410)
def page_not_found(error):
    content = json.dumps({"error_code": "410"})
    resp = Response_headers(content)
    return resp

@app.errorhandler(500)
def page_not_found(error):
    content = json.dumps({"error_code": "500"})
    resp = Response_headers(content)
    return resp

if __name__ == '__main__':
  app.run(debug=True)
