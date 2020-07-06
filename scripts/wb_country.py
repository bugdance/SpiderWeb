#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymysql
import urllib.request
import json
import time
import threading
import socket


conn = pymysql.connect( host='localhost', port=33306, \
                        user='root', passwd='logis2017', \
                        db='db_data', charset='utf8')
cur = conn.cursor()
    
#url = 'http://api.worldbank.org/countries?per_page=500&format=json'
url = 'http://api.worldbank.org/zh/countries?per_page=500&format=json'
time.sleep(2)
if socket.setdefaulttimeout(30):
    print(2)
try:
    page=urllib.request.urlopen(url)
    d=json.loads(page.read().decode('utf-8'))
except Exception as e:
    print(1)
else:
    for i in d[1]:
#        cur.execute("insert ignore into data_wb_countries(iso3code,iso2code,country_name,cn_zh,capital_city,cc_zh,region_id,region_value,rv_zh,adminregion_id,adminregion_value,av_zh,incomelevel_id,incomelevel_value,iv_zh,lendingtype_id,lendingtype_value,lv_zh,longitude,latitude) values(%s,%s,%s,'',%s,'',%s,%s,'',%s,%s,'',%s,%s,'',%s,%s,'',%s,%s)", (i['id'],i['iso2Code'],i['name'],i['capitalCity'],i['region']['id'],i['region']['value'],i['adminregion']['id'],i['adminregion']['value'],i['incomeLevel']['id'],i['incomeLevel']['value'],i['lendingType']['id'],i['lendingType']['value'],i['longitude'],i['latitude']))     
        cur.execute("update data_wb_countries set cn_zh=%s,cc_zh=%s,rv_zh=%s,av_zh=%s,iv_zh=%s,lv_zh=%s where iso3code=%s", (i['name'],i['capitalCity'],i['region']['value'],i['adminregion']['value'],i['incomeLevel']['value'],i['lendingType']['value'],i['id']))     
        conn.commit()

cur.close()
conn.close()
