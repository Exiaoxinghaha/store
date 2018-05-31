from django.contrib import admin
from shop.models import GoodsInfo,GoodsCategory,GoodsArea

@admin.register(GoodsInfo)
class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 20
    search_fields = ['name','detail','description']
    # fields = ['detail'] #包括字段
    list_filter = ['category','area']
    exclude = ['id']    #排除字段

@admin.register(GoodsCategory)
class GoodsCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(GoodsArea)
class GoodsAreaAdmin(admin.ModelAdmin):
    search_fields = ['name']
