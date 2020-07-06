#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import sys
import pymysql
import imp

imp.reload(sys)
conn = pymysql.connect( host='localhost', port=33306, \
                        user='root', passwd='logis2017', \
                        db='db_data', charset='utf8')
cur = conn.cursor()

a= cur.execute("select sid from data_city_codes where level=2 or level=3 ORDER BY sid")
b= cur.fetchmany(a)

for i in b:
    c = list(i)
    for j in b:
        d = list(j)
        cur.execute("insert ignore into data_kd100_url(send_code,receive_code,update_number) values(%s,%s,0)", (c[0],d[0]))
        conn.commit()
cur.close()
conn.close()

