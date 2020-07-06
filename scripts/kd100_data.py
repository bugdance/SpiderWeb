#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import pymysql
import urllib.request
import json
import time
import threading
import socket


def freight(num):
    conn = pymysql.connect( host='localhost', port=33306, \
                            user='root', passwd='logis2017', \
                            db='db_data', charset='utf8')
    cur = conn.cursor()
    
    a= cur.execute("select id,send_code,receive_code from data_kd100_url where update_number = %s"%num)
    b= cur.fetchmany(a)
    
    for i in b:
        c = list(i)
        url = 'http://www.kuaidi100.com/order/unlogin/price.do?action=searchOrderPrice&currentPage=1& \
        pageSize=100&delivery=YES&deliveryType=TO_DOOR&endPlace_input=&startPlace_input=&street=& \
        vistReceive=YES&weight=1&startPlace=%s&endPlace=%s'%(c[1],c[2])
        time.sleep(3)
        if socket.setdefaulttimeout(30):
            cur.execute("update data_kd100_url set update_number=4 where id=%s"%c[0])
            conn.commit()
        try:
            page=urllib.request.urlopen(url)
            d=json.loads(page.read().decode('utf-8'))
        except Exception as e:
            cur.execute("update data_kd100_url set update_number=4 where id=%s"%c[0])
            conn.commit()
        else:
            try:
                d['orderList']
            except Exception as e:
                cur.execute("update data_kd100_url set update_number=3 where id=%s"%c[0])
                conn.commit()
            else:
                if d['orderList'] != []:
                    for j in d['orderList']:
                        p = j['priceInfo']
                        v = j['valueAdds']
                        if p['type'] == 'EXPRESS':        
                            if p['expressCode'] != '':
                                com_code = p['expressCode']
                            else:
                                com_code = p['companyCode']
                            
                            cur.execute("insert ignore into data_kd100_express(company_code,product_type, \
                            send_code,receive_code,pick_time,freight_time,total_price,min_price,first_price, \
                            follow_price,phone,qq) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (com_code, \
                            p['productType'],c[1],c[2],p['pTimeFrom']+'-'+p['pTimeTo'],p['time'],p['totalPrice'], \
                            p['minprice'],p['firstprice'],p['followprice'],p['tel'],p['qq']))     
                            conn.commit()
                        elif p['type'] == 'LOGISTICS':        
                            pass
                        else:
                            continue
                    cur.execute("update data_kd100_url set update_number=1 where id=%s"%c[0])
                    conn.commit()
                else:
                    cur.execute("update data_kd100_url set update_number=2 where id=%s"%c[0])
                    conn.commit()
    
    
     
    
    cur.close()
    conn.close()


threads = []
thr = threading.Thread(target=freight, args=(9,))
threads.append(thr)


if __name__ == '__main__':
    for tt in threads:
            tt.setDaemon(True)
            tt.start()

    tt.join()
