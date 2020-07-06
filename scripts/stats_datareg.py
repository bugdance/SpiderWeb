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
cur2 = conn.cursor()
db = cur.execute("select dbcode,sid from data_stats_types where wdcode='zb' and isparent=0 \ 
        and dbcode in ('fsyd','fsjd','fsnd','csyd','csnd','gjyd','gjnd')")
db2 = cur2.execute("select distinct dbcode,sid from data_stats_types where wdcode='reg' and level=0")
line = cur.fetchmany(db)
line2 = cur2.fetchmany(db2)


for i in line:
    url = ('http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=%s&rowcode=zb&colcode=sj&dfwds=[{"wdcode":"zb","valuecode":"%s"},' % (i[0],i[1]))
    for j in line2:
        if j[0] == i[0]:
            url2 = url + ('{"wdcode":"sj","valuecode":"LAST100"}]&wds=[{"wdcode":"reg","valuecode":"%s"}]' % j[1])

            time.sleep(1)
            if socket.setdefaulttimeout(30):
                continue

            page = urllib.request.urlopen(url2)
            try:
                data = json.loads(page.read().decode('utf-8'))
            except Exception as e:
                continue
            else:
                try:
                    d = data['returndata']['datanodes']
                    w = data['returndata']['wdnodes'][0]['nodes']
                    w1 = data['returndata']['wdnodes'][2]['nodes']
                except Exception as e:
                    continue
                else:
                    for m in range(0,len(w)):
                        cur.execute("insert ignore into data_stats_types(dbcode, sid, isparent, name, exp,pid,wdcode,unit,level,memo)" \
                            "values(%s, %s, 0, %s, %s,%s, 'zb',%s,0,%s)", (i[0],w[m]['code'],w[m]['name'],w[m]['exp'],i[1],w[m]['unit'],w[m]['memo']))
                        conn.commit()

                    for k in range(0,len(d)):
                        for l in range(0,len(w1)):
                            if d[k]['wds'][2]['valuecode']==w1[l]['code']:
                                cur.execute("insert into data_stats_data(dbcode,pid,sid, strdata, valuecode,regcode)" \
                                "values(%s,%s,%s,%s, %s, %s) on duplicate key update strdata=strdata+1", \
                                 (i[0],i[1],d[k]['wds'][0]['valuecode'],d[k]['data']['strdata'],d[k]['wds'][2]['valuecode'],j[1]))
                                conn.commit()
        else:
            continue

cur.close()
cur2.close()
conn.close()

del cur,cur2, conn, db,db2, line,line2 
gc.collect()
