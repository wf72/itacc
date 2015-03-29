# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from addressbook import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^(?P<contact_id>\d+)/$', views.detail, name='detail'),
                       # # ex: /polls/5/results/
                       # url(r'^(?P<contact_id>\d+)/results/$', views.results, name='results'),
                       # # ex: /polls/5/vote/
                       url(r'^(?P<contact_id>\d+)/edit/$', views.edit, name='edit'),
                       # url(r'^(?P<contact_id>\d+)/editpost/$', views.editpost, name='editpost'),
                       url(r'^(?P<contact_id>\d+)/del/$', views.delete, name='delete'),
                       url(r'^editpost/$', views.editpost, name='editpost'),
                       url(r'^add/$', views.add, name='add'),
                       url(r'^login/$', login, name='login'),
                       url(r'^logout/$', logout, name='logout'),
                       url(r'^sync_ldap/$', views.ldap_sync, name='sync_ldap'),

                       )