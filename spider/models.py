#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible
import json
import pymysql

# Create your models here.

def validate_json(value):
    try:
        json_value = json.loads(value)
    except Exception as e:
        raise ValidationError("输入一个有效的Json格式文件")
    else:
        pass

def validate_name(value):
    conn = pymysql.connect(host='127.0.0.1', port=33306, user='root', passwd='logis2017', db='website', charset='utf8')
    cur = conn.cursor()
    if cur.execute("select * from spider_configs where config_name='%s'" % value):
        pass
    else:
        raise ValidationError("没有此文件")
    conn.close()

@python_2_unicode_compatible
class Configs(models.Model):
    config_name = models.CharField(verbose_name='配置名称', help_text='格式为news_search_163', default='', unique=True, max_length=100)
    site_name = models.CharField(verbose_name='网站名称', help_text='请填写准确以方便查询', default='', max_length=100)
    site_domain = models.URLField(verbose_name='网站域名', help_text='格式为music.163.com', default='', max_length=100)
    config_text = models.TextField(verbose_name='配置内容', help_text='Json格式文件键和值请用 " 双引号', default='', validators=[validate_json])
    config_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    def __str__(self):
        return '配置文件'

    class Meta:
        db_table = 'spider_configs'
        verbose_name = '配置文件'
        verbose_name_plural = '配置文件'

@python_2_unicode_compatible
class Tasks(models.Model):

    CHO_IP = (('182.92.75.82', '182'), ('43.243.136.230', '230'),)
    CHO_PORT = ((36800, '36800'), (36900, '36900'),)
    CHO_PRJ = (('example', '项目1'), ('project2', '项目2'),)
    CHO_SPD = (('example', '爬虫1'), ('spider2', '爬虫2'),)
    config_name = models.CharField(verbose_name='配置名称', help_text='请填写配置文件里已有的文件名称', default='', max_length=100, validators=[validate_name])
    bot_ip = models.GenericIPAddressField(verbose_name='目标地址', default='0.0.0.0', choices=CHO_IP)
    bot_port = models.IntegerField(verbose_name='目标端口', default=0, choices=CHO_PORT)
    project_name = models.CharField(verbose_name='项目名称', default='', max_length=100, choices=CHO_PRJ)
    spider_name = models.CharField(verbose_name='爬虫名称', default='', max_length=100, choices=CHO_SPD)
    task_time = models.DateTimeField(verbose_name='任务时间', auto_now_add=True)
    job_id = models.CharField(verbose_name='工作序号', default=0, editable=False, max_length=200)
    task_run = models.IntegerField(verbose_name='任务发送', default=0, editable=False)

    def __str__(self):
        return '任务管理'

    class Meta:
        db_table = 'spider_tasks'
        verbose_name = '任务管理'
        verbose_name_plural = '任务管理'


@python_2_unicode_compatible
class Monitors(models.Model):
    job_id = models.CharField(verbose_name='工作序号', default='', unique=True, editable=False, max_length=200)
    bot_ip = models.GenericIPAddressField(verbose_name='机器地址', default='0.0.0.0', editable=False)
    bot_name = models.CharField(verbose_name='项目名称', default='', editable=False, max_length=100)
    spider_name = models.CharField(verbose_name='爬虫名称', default='', editable=False, max_length=100)
    config_path = models.CharField(verbose_name='配置名称', default='', editable=False, max_length=100)
    finish_reason = models.CharField(verbose_name='完成原因', default='', editable=False, max_length=100)
    dropped_count = models.IntegerField(verbose_name='丢掉数目', default=0, editable=False)
    scraped_count = models.IntegerField(verbose_name='采集数目', default=0, editable=False)
    start_time = models.DateTimeField(verbose_name='开始时间', editable=False)
    finish_time = models.DateTimeField(verbose_name='结束时间', editable=False)
    elapsed_time = models.IntegerField(verbose_name='运行时长', default=0, editable=False)

    def __str__(self):
        return '监测管理'

    class Meta:
        db_table = 'spider_monitors'
        verbose_name = '监测管理'
        verbose_name_plural = '监测管理'


@python_2_unicode_compatible
class Proxy(models.Model):
    protocol = models.CharField(verbose_name='网络协议', default='http', editable=False, max_length=50)
    ip = models.GenericIPAddressField(verbose_name='网络地址', default='127.0.0.1', editable=False)
    port = models.IntegerField(verbose_name='网络端口', default=80, editable=False)
    website = models.CharField(verbose_name='抓取网站', default='', editable=False, max_length=50)
    ifadd = models.IntegerField(verbose_name='是否添加', default=0, editable=False)

    def __str__(self):
        return '代理地址'
    class Meta:
        db_table = 'spider_proxy'
        unique_together = ('protocol', 'ip', 'port')
        verbose_name = '代理地址'
        verbose_name_plural = '代理地址'


@python_2_unicode_compatible
class Keyword(models.Model):
    word = models.CharField(verbose_name='关键词语', help_text='限制100字内', default='', unique=True, max_length=100)
    ifadd = models.IntegerField(verbose_name='是否添加', default=0, editable=False)

    def __str__(self):
        return '关键词语'
    class Meta:
        db_table = 'spider_keyword'
        verbose_name = '关键词语'
        verbose_name_plural = '关键词语'
