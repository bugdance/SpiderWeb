#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymysql
import urllib.request
import json
import time
import threading
import socket
import gc


def data(num):
    conn = pymysql.connect( host='localhost', port=33306, \
                            user='root', passwd='logis2017', \
                            db='db_data', charset='utf8')
    cur = conn.cursor()
    
    a= cur.execute("select id,iso2code,indicator_id from data_wb_url where update_number = %s"%num)
    b= cur.fetchmany(a)
    
    for i in b:
        c = list(i)
        url = 'http://api.worldbank.org/countries/%s/indicators/%s?per_page=100&format=json'%(c[1],c[2])
        time.sleep(2)
        if socket.setdefaulttimeout(60):
            cur.execute("update data_wb_url set update_number=4 where id=%s"%c[0])
            conn.commit()
        try:
            page=urllib.request.urlopen(url)
            d=json.loads(page.read().decode('utf-8'))
        except Exception as e:
            cur.execute("update data_wb_url set update_number=4 where id=%s"%c[0])
            conn.commit()
        else:
            try:
                d[1]
            except Exception as e:
                cur.execute("update data_wb_url set update_number=3 where id=%s"%c[0])
                conn.commit()
            else:
                if d[1] == None or '' or []:
                    cur.execute("update data_wb_url set update_number=2 where id=%s"%c[0])
                    conn.commit()
                    continue
                else:
                    for j in d[1]:
                        if j['value'] == None or '':
                            cur.execute("insert ignore into data_wb_data(iso2code,indicator_id,valuecode,strdata) values(%s,%s,%s,0)", (c[1],c[2],j['date']))     
                            conn.commit()
                        else:
                            cur.execute("insert ignore into data_wb_data(iso2code,indicator_id,valuecode,strdata) values(%s,%s,%s,%s)", (c[1],c[2],j['date'],j['value']))     
                            conn.commit()
                    cur.execute("update data_wb_url set update_number=1 where id=%s"%c[0])
                    conn.commit()
    
    
     
    
    cur.close()
    conn.close()
    del a, b, conn, cur, c, d, t, url, page
    gc.collect()

threads = []
thr = threading.Thread(target=data, args=(0,))
threads.append(thr)


if __name__ == '__main__':
    for tt in threads:
            tt.setDaemon(True)
            tt.start()

    tt.join()
