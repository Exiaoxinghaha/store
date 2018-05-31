from django.contrib import admin
from shoporder.models import OrderMain,OrderDetail

@admin.register(OrderMain)
class OrderMainAdmin(admin.ModelAdmin):
    list_display = ['user','order_number','status']
    search_fields = ['user','order_number']

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['goods_info','order','goods_price','count','total']
    search_fields = ['goods_info','order']

