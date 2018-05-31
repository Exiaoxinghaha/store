# -*-coding:utf-8-*-
from .models import ShopCart
from .cache import User_Cart_Cache

def goods_num(request):
    sessionid = request.COOKIES.get('mysessionid')
    shopcartcache = User_Cart_Cache()
    if not request.user.is_authenticated:
        goods_num = shopcartcache.get_cart_len_cache(sessionid)
        return {'goods_num':goods_num}
    # 登录之后把缓存数据合并到数据库
    goods = shopcartcache.getall_goods_cache(sessionid)
    if goods:
        for gid,buy_num in goods.items():
            shopcart,is_create = ShopCart.objects.update_or_create(user=request.user,goodinfo_id=gid)
            shopcart.buy_num = int(buy_num)
            shopcart.save()
            shopcartcache.delete_goods_cache(sessionid,gid)
    goods_num = ShopCart.objects.filter(user=request.user,status=0).count()
    return {'goods_num':goods_num}