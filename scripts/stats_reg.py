#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymysql
import urllib.request
import json
import time
import gc

#connect to mysql

conn = pymysql.connect(	host='localhost', port=33306, \
						user='root', passwd='logis2017', \
						db='db_data', charset='utf8')
cur = conn.cursor()

#db = cur.execute("select dbcode,sid from data_stats_types where isParent=1 and wdcode='reg' and level=1")
#line = cur.fetchmany(db)
#
#
#for k in line:
#    url = ("http://data.stats.gov.cn/easyquery.htm?dbcode=%s&m=getTree&wdcode=reg&id=%s" % (k[0],k[1]))
#    time.sleep(2)
#
#    page = urllib.request.urlopen(url)
#    try:
#        data = json.loads(page.read().decode('utf-8'))
#    except Exception as e:
#        continue
#    else:
#        for i in range(0,len(data)):
#            p = data[i]
#            cur.execute("insert ignore into data_stats_types(dbcode, sid, isParent, name, pid,wdcode,level, unit,exp,memo)" \
#                        "values(%s, %s, %s, %s, %s, %s,2,'','','')", (p['dbcode'],p['id'],p['isParent'],p['name'],p['pid'],p['wdcode']))

db = cur.execute("select dbcode,sid from data_stats_types where isparent=0 and wdcode='reg'")
line = cur.fetchmany(db)

for l in line:
    url = ('http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=%s&rowcode=reg&colcode=sj&wds=[]&dfwds=[{"wdcode":"reg","valuecode":"%s"}]' % (l[0],l[1]))
    time.sleep(2)

    page = urllib.request.urlopen(url)
    try:
        data = json.loads(page.read().decode('utf-8'))
    except Exception as e:
        continue
    else:
        try:
            w = data['returndata']['wdnodes'][1]['nodes']
        except Exception as e:
            continue
        else:
            for j in range(0,len(w)):
                cur.execute("insert ignore into data_stats_types(dbcode, sid, isparent, name, pid,wdcode,unit, level,exp,memo)" \
                            "values(%s, %s, 0,%s, %s, 'reg',%s,0,'','')", (l[0],w[j]['code'],w[j]['name'],l[1],w[j]['unit']))



conn.commit()
cur.close()
conn.close()

del cur, conn, line, url, page
gc.collect()
