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
#topics total 21   
for t in range(1,22):

    #url = 'http://api.worldbank.org/topics/%s/indicators?per_page=500&format=json&page=1' % t
    url = 'http://api.worldbank.org/zh/topics/%s/indicators?per_page=500&format=json&page=1' % t
    try:
        time.sleep(5)
        page=urllib.request.urlopen(url)
        if socket.setdefaulttimeout(60):
            print(2)
        d=json.loads(page.read().decode('utf-8'))
    except Exception as e:
        print(1)
    else:
        for i in d[1]:
            for j in range(0,len(i['topics'])):
#                cur.execute("insert ignore into data_wb_topics(indicator_id,indicator_name,in_zh,topic_id,topic_value,tv_zh,source_note,sn_zh,source_organization,so_zh) values(%s,%s,'',%s,%s,'',%s,'',%s,'')", (i['id'],i['name'],i['topics'][j]['id'],i['topics'][j]['value'],i['sourceNote'],i['sourceOrganization']))     
                cur.execute("update data_wb_topics set in_zh=%s,tv_zh=%s,sn_zh=%s,so_zh=%s where indicator_id=%s and topic_id=%s", (i['name'],i['topics'][j]['value'],i['sourceNote'],i['sourceOrganization'],i['id'],i['topics'][j]['id']))     
                conn.commit()

cur.close()
conn.close()
