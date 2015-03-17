from django.contrib import admin
from django.contrib.admin import AdminSite
from addressbook.models import Contact
from addressbook.models import Ldap_settings
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('lastname','firstname','position','phone','email')
    list_filter = ['lastname','active']
    search_fields = ['lastname','firstname','position','phone','email']

class LdapAdmin(admin.ModelAdmin):
    list_display = ('ldap_server','ldap_user','ldap_base','active')

class MyAdminSite(AdminSite):
    site_header = "asd"
    site_title = "vcx"

admin.site.register(Contact,ContactAdmin)
admin.site.register(Ldap_settings,LdapAdmin)