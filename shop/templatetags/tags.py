# -*-coding:utf-8-*-
from django import template
from shop.models import GoodsInfo
from django.conf import settings

register = template.Library()

@register.inclusion_tag('shop/refferral_good.html')
def refferral_good(cid=None):
    if cid:
        refferral_goods = GoodsInfo.objects.filter(category_id=cid).order_by('-id').all()[:2]
    else:
        refferral_goods = GoodsInfo.objects.order_by('-id').all()[:2]
    return {
        'refferral_goods':refferral_goods,
        'MEDIA_URL':settings.MEDIA_URL
    }