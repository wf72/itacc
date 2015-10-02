from django.contrib import admin

from cashbox.models import CashBoxSetting, CashBox, CashboxPermission, Shop, User

class CashBoxSettingAdmin(admin.ModelAdmin):
    save_as = True

class CashBoxAdmin(admin.ModelAdmin):
    save_as = True

class CashboxPermissionAdmin(admin.ModelAdmin):
    save_as = True

class ShopAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'cashbox_permission')
    list_filter = ['cashbox',]
    search_fields = ('name', 'cashbox')

admin.site.register(CashBoxSetting, CashBoxSettingAdmin)
admin.site.register(CashBox, CashBoxAdmin)
admin.site.register(CashboxPermission, CashboxPermissionAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(User, UserAdmin)