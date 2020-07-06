#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymysql
import urllib.request
import json
import time
import gc
import socket

#connect to mysql

conn = pymysql.connect(	host='localhost', port=33306, \
						user='root', passwd='logis2017', \
						db='db_data', charset='utf8')
cur = conn.cursor()
db = cur.execute("select dbcode,sid from data_stats_types where isparent=0 and wdcode='zb' and dbcode in ('hgyd','hgjd','hgnd')")
line = cur.fetchmany(db)


for i in line:
    url = ('http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=%s&rowcode=zb&colcode=sj&wds=[]&dfwds=[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"LAST100"}]' % (i[0],i[1]))

    time.sleep(1)
    if socket.setdefaulttimeout(30):
        continue

    page = urllib.request.urlopen(url)
    try:
        data = json.loads(page.read().decode('utf-8'))
    except Exception as e:
        continue
    else:
        try:
            d = data['returndata']['datanodes']
            w = data['returndata']['wdnodes'][0]['nodes']
            w1 = data['returndata']['wdnodes'][1]['nodes']
        except Exception as e:
            continue
        else:
            
            for j in range(0,len(w)):
                cur.execute("insert ignore into data_stats_types(dbcode, sid, isparent, name, exp,pid,wdcode,unit,level,memo)" \
                            "values(%s, %s, 0,%s, %s,%s, 'zb',%s,0,%s)", (i[0],w[j]['code'],w[j]['name'],w[j]['exp'],i[1],w[j]['unit'],w[j]['memo']))
                conn.commit()
            

            for k in range(0,len(d)):
                for l in range(0,len(w1)):
                    if d[k]['wds'][1]['valuecode']==w1[l]['code']:
                        cur.execute("insert into data_stats_data(dbcode,pid, sid, strdata, valuecode,regcode)" \
                        "values(%s,%s,%s,%s,%s,0) on duplicate key update strdata=strdata+1", (i[0],i[1],d[k]['wds'][0]['valuecode'],d[k]['data']['strdata'],d[k]['wds'][1]['valuecode']))
                        conn.commit()

cur.close()
conn.close()

del cur, conn, db, line, url, page
gc.collect()
