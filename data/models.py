#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models


# Create your models here.
@python_2_unicode_compatible
class City_Codes(models.Model):
    sid = models.IntegerField(verbose_name='本级代码', default=0, unique=True)
    pid = models.IntegerField(verbose_name='父级代码', default=0)
    full_name = models.CharField(verbose_name='本级全称', default='', max_length=50)
    level = models.IntegerField(verbose_name='本级级别', default=0)

    def __str__(self):
        return '城市数据'

    class Meta:
        db_table = 'data_city_codes'
        verbose_name = '城市数据'
        verbose_name_plural = '城市数据'

#@python_2_unicode_compatible
#class Wldl_News(models.Model):
#    article_url = models.URLField(verbose_name='链接地址', default='', max_length=250)
#    article_title = models.CharField(verbose_name='文章标题', default='', max_length=100)
#    article_time = models.DateField(verbose_name='发表时间')
#    article_src = models.CharField(verbose_name='发表来源', default='', max_length=100)
#    article_content = models.TextField(verbose_name='发表内容', default='')
#    website = models.CharField(verbose_name='抓取网站', default='', max_length=100)
#    search_word = models.CharField(verbose_name='搜索文字', default='', max_length=100)
#    scraped_time = models.DateField(verbose_name='抓取时间')
#    visit_count = models.IntegerField(verbose_name='点击次数', default=0)
#    share_count = models.IntegerField(verbose_name='分享次数', default=0)
#    reply_count = models.IntegerField(verbose_name='回复次数', default=0)
#    favorite_count = models.IntegerField(verbose_name='点赞次数', default=0)
#    isreply = models.IntegerField(verbose_name='是否是回复贴', default=0)
#
#    def __str__(self):
#        return '资讯数据'
#
#    class Meta:
#        db_table = 'data_wldl_news'
#        unique_together = ('article_title', 'article_src', 'article_time', 'website')
#        verbose_name = '物流地理资讯数据'
#        verbose_name_plural = '物流地理资讯数据'
#
#
#
