#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import pymysql
import urllib.request
import json
import time
import gc


def base():
    conn = pymysql.connect( host='localhost', port=33306, \
                            user='root', passwd='logis2017', \
                            db='db_data', charset='utf8')
    cur = conn.cursor()
    
#### zb指标 ###    
#    kw=['hgyd','hgjd','hgnd','fsyd','fsjd','fsnd','csyd','csnd','gjyd','gjnd']
#    
#    for k in kw:
#        url = ('http://data.stats.gov.cn/easyquery.htm?dbcode=%s&m=getTree&wdcode=zb&id=zb') % k
#        time.sleep(2)
#    
#        page = urllib.request.urlopen(url)
#        try:
#            data = json.loads(page.read().decode('utf-8'))
#        except Exception as e:
#            continue
#        else:
#            for i in range(0,len(data)):
#                p = data[i]
#                cur.execute("insert ignore into data_stats_types(dbcode, sid, isparent, name, pid,wdcode,level,unit,exp,memo)" \
#                            "values(%s, %s, %s, %s, %s, %s,1,'','','')", (p['dbcode'],p['id'],p['isParent'],p['name'],p['pid'],p['wdcode']))


###  reg指标  ###
    kw=['fsyd','fsjd','fsnd','csyd','csnd','gjyd','gjnd']
    
    for k in kw:
        url = ('http://data.stats.gov.cn/easyquery.htm?dbcode=%s&m=getTree&wdcode=reg&id=reg') % k
        time.sleep(2)
    
        page = urllib.request.urlopen(url)
        try:
            data = json.loads(page.read().decode('utf-8'))
        except Exception as e:
            continue
        else:
            for i in range(0,len(data)):
                p = data[i]
                cur.execute("insert ignore into data_stats_types(dbcode, sid, isParent, name, pid,wdcode,level,unit,exp,memo)" \
                            "values(%s, %s, %s, %s, %s, %s,1,'','','')", (p['dbcode'],p['id'],p['isParent'],p['name'],p['pid'],p['wdcode']))
    conn.commit()
    cur.close()
    conn.close()
    
    del cur, conn, kw, url, page
    gc.collect()

base()
