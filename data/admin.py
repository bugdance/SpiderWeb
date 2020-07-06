#-*- coding: utf-8 -*-

from __future__ import unicode_literals


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import City_Codes
# Register your models here.

@admin.register(City_Codes)
class City_CodesAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_display = ('sid', 'pid', 'full_name', 'level')
    list_filter = ['sid', 'pid', 'level']
    list_per_page = 50
    ordering = ['level']


#@admin.register(Wldl_News)
#class Wldl_NewsAdmin(admin.ModelAdmin):
#    readonly_fields = ('article_title', 'article_time', 'article_src', 'article_content', 'website', 'article_url', 'search_word', 'visit_count', 'share_count', 'reply_count', 'favorite_count', 'isreply', 'scraped_time')
#    search_fields = ['article_title']
#    list_display = ('article_title', 'article_time', 'article_src', 'search_word', 'website', 'scraped_time')
#    list_filter = ('website', 'search_word', 'article_time', 'scraped_time')
#    list_filter = ('website', 'search_word')
#    list_per_page = 50
#    ordering = ['-article_time']



