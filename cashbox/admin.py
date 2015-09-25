from django.contrib import admin

from cashbox.models import CashBoxSetting, CashBox, CashboxPermission, Shop, User


# Register your models here.

class CashBoxSettingAdmin(admin.ModelAdmin):
    pass

class CashBoxAdmin(admin.ModelAdmin):
    pass

class CashboxPermissionAdmin(admin.ModelAdmin):
    pass

class ShopAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(CashBoxSetting, CashBoxSettingAdmin)
admin.site.register(CashBox, CashBoxAdmin)
admin.site.register(CashboxPermission, CashboxPermissionAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(User, UserAdmin)