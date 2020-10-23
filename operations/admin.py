from django.contrib import admin

# Register your models here.

from django.contrib import admin
from . import models

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'gam_account_no', 'order_id', 'order_name')
    search_fields = ('gam_account_no', 'order_id', 'order_name')

class LineItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'li_id', 'li_name', 'li_price', 'li_status')
    search_fields = ('id', 'order', 'li_id', 'li_name', 'li_price', 'li_status')

admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.LineItem, LineItemAdmin)