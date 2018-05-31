# -*-coding:utf-8-*-
from .models import GoodsCategory

def categorys(request):
    categorys = GoodsCategory.objects.filter(status=0).all()
    return {'categroys':categorys}