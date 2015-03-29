from django.contrib import admin
from django.contrib.admin import AdminSite
from addressbook.models import Contact
from addressbook.models import Settings
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'position', 'phone', 'email')
    list_filter = ['lastname', 'active']
    search_fields = ['lastname', 'firstname', 'position', 'phone', 'email']


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')


class MyAdminSite(AdminSite):
    site_header = "asd"
    site_title = "vcx"


admin.site.register(Contact, ContactAdmin)
admin.site.register(Settings, SettingsAdmin)