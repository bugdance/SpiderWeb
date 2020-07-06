#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import Configs, Tasks, Monitors, Proxy, Keyword
import json
import pymysql
import subprocess
# Register your models here.

Conn = pymysql.connect( host='localhost', port=33306, user='root',passwd='logis2017',db='website',charset='utf8')

@admin.register(Configs)
class ConfigsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('查询设置', {
            'fields': ('site_domain','site_name')
        }),
        ('内容设置', {
            'fields': ('config_text','config_name')
        }),
    )
    list_display = ['site_name', 'config_name', 'site_domain', 'config_date']
    search_fields = ['site_name']
    list_filter = ['config_name', 'site_domain', 'config_date']
    list_per_page = 50

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    def task_log(self):
        return u"<a href='http://%s:%s/logs/%s/%s/%s.log'>查看Log</a><br>" % \
            (self.bot_ip, self.bot_port, self.project_name, self.spider_name, self.job_id)
    task_log.short_description = 'Log日志'
    task_log.allow_tags = True
   
    fieldsets = (
        ('参数设置', {
            'fields': ('config_name', 'bot_ip', 'bot_port', 'project_name', 'spider_name')
        }),
    )
    list_display = ('job_id', 'config_name', 'bot_ip', 'project_name', 'spider_name', 'task_time', task_log)
    list_display_links = None
    search_fields = ['task_time']
    list_filter = ['task_time']
    list_per_page = 30
    actions = ['run']

    def run(self, request, queryset):
        
        queryset.update(task_run=2)
        connMy = pymysql.connect( host='localhost', port=33306, user='root',passwd='logis2017',db='website',charset='utf8')
        curMy = connMy.cursor() 
        
        curMy.execute("select id,config_name,bot_port,project_name,spider_name,bot_ip from spider_tasks where task_run=2")
        data = curMy.fetchall()
        for row in data: 
            command = 'curl http://%s:%s/schedule.json -d project=%s -d spider=%s' \
                            ' -d config=/var/www/spider.56dili.cn/configs/%s.conf' % (row[5],row[2], row[3], row[4], row[1])
            p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out, err = p.communicate()
            cjson = json.loads(out.decode('utf-8'))

            curMy.execute("update spider_tasks set job_id=%s where id=%s", (cjson['jobid'],row[0]))
            connMy.commit()
        queryset.update(task_run=1)
        self.message_user(request, "成功执行!")
        
        curMy.close()
        connMy.close()
    run.short_description = '运行'


@admin.register(Monitors)
class MonitorsAdmin(admin.ModelAdmin):

    readonly_fields = ('job_id', 'bot_ip', 'bot_name', 'spider_name', 'config_path', 'finish_reason', 'dropped_count', 'scraped_count', 'start_time', 'finish_time', 'elapsed_time')
    search_fields = ['config_name']
    list_display = ('job_id', 'spider_name', 'config_path', 'finish_reason', 'dropped_count', 'scraped_count', 'start_time', 'finish_time')
    list_display_links = None
    list_filter = ['finish_reason', 'start_time', 'finish_time']
    list_per_page = 30


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):

    def addproxy(self, request, queryset):
        queryset.update(ifadd=1)
        connMy = pymysql.connect( host='localhost', port=33306, user='root',passwd='logis2017',db='website',charset='utf8')
        curMy = connMy.cursor() 
        
        curMy.execute("select protocol, ip, port from spider_proxy where ifadd=1")
        data = curMy.fetchall()
        f = open('/var/www/spider.56dili.cn/configs/proxy.txt', 'w')
        for row in data:
            print >> f, str(row[0])+' '+str(row[1])+' '+str(row[2])
        f.close()
        queryset.update(ifadd=0)
        
        curMy.close()
        connMy.close()
    addproxy.short_description = '添加代理到配置中'
    actions = [addproxy]


    readonly_fields = ('protocol', 'ip', 'port', 'website')
    list_display = ['protocol', 'ip', 'port', 'website']
    search_fields = ['website']
    list_filter = ['protocol', 'ip', 'port']
    list_per_page = 30


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    def addword(self, request, queryset):
        queryset.update(ifadd=1)
        connMy = pymysql.connect( host='localhost', port=33306, user='root',passwd='logis2017',db='website',charset='utf8')
        curMy = connMy.cursor() 
        
        curMy.execute("select word from spider_keyword where ifadd=1")
        data = curMy.fetchall()
        f = open('/var/www/spider.56dili.cn/configs/keyword.txt', 'w')
        for row in data:
            print >> f, str(row[0].encode('utf8'))
        f.close()
        queryset.update(ifadd=0)
        
        curMy.close()
        connMy.close()
    addword.short_description = '添加词语到配置中'
    actions = [addword]


    list_display = ['word']
    search_fields = ['word']
    list_per_page = 30
