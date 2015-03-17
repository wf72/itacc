from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'itacc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^addressbook/', include('addressbook.urls',namespace="addressbook")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',  login),
    (r'^logout/$', logout),
)
