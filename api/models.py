#-*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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
