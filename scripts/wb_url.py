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

a= cur.execute("select distinct indicator_id from data_wb_topics")
b= cur.fetchmany(a)

a1= cur.execute("select iso2code from data_wb_countries where region_id != 'NA'")
b1= cur.fetchmany(a1)

for i in b:
    c = list(i)
    for j in b1:
        d = list(j)
        cur.execute("insert ignore into data_wb_url(indicator_id,iso2code,update_number) values(%s,%s,0)", (c[0],d[0]))
        conn.commit()

cur.close()
conn.close()

