from django.contrib import admin
from .models import MiniSetting


class MiniSettingAdmin(admin.ModelAdmin):  
    list_display = ['name', 'type', 'value']


admin.site.register(MiniSetting, MiniSettingAdmin)
