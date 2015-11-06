# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

from cashbox import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^settings/$', views.rendersettings, name='rendersettings'),
                       url(r'cashbox_users/(?P<cashbox_id>\d+)', views.cashbox_users, name='cashbox_users'),
                       url(r'^login/$', login, name='login'),
                       url(r'^logout/$', logout, name='logout'),
                       )
