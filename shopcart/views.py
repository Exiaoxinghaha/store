from django.shortcuts import render,redirect,reverse
from django.views import View
from shop.models import GoodsInfo
from account.models import UserProfile
from django.http import JsonResponse
from .models import ShopCart
from .cache import User_Cart_Cache
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from utils.exception import StockException
from utils.order_code import order_code
from shoporder.models import OrderMain,OrderDetail

# 购物车视图
class ShopCartView(View):
    def get(self,request):
        if request.user.is_authenticated:
            cart_info = ShopCart.objects.filter(user=request.user,status=0).all()
        else:
            cart_info = []
            shopcartcache = User_Cart_Cache()
            sessionid = request.COOKIES.get('mysessionid')
            goods = shopcartcache.getall_goods_cache(sessionid) # 得到字典类型的商品数据
            for gid,buy_num in goods.items():
                cart_info.append({
                    'goodinfo' : GoodsInfo.objects.get(pk=gid),
                    'buy_num' : int(buy_num),
                })
        return render(request,'shop_cart/cart.html',locals())
    def post(self,request):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        cart_by_goods_ids = request.POST.getlist('cart_by_goods_id')
        cart_by_goods_id = []
        for gid in cart_by_goods_ids:
            shopcart = ShopCart.objects.get(goodinfo_id=gid)
            cart_by_goods_id.append(shopcart.pk)
        shopcart = ShopCart.objects.in_bulk(id_list=cart_by_goods_id)# 返回对象的集合
        assert len(shopcart.keys()) == len(cart_by_goods_id)
        try:
            with transaction.atomic():
                ordermain = OrderMain(order_number=order_code(),user=request.user,total=0)
                ordermain.save()
                for shopcart in shopcart.values():
                    orderdetail = OrderDetail()
                    orderdetail.order = ordermain
                    orderdetail.goods_info = shopcart.goodinfo
                    orderdetail.goods_price = float(shopcart.goodinfo.price)
                    if shopcart.buy_num > shopcart.goodinfo.stock:
                        message = '{}库存不足哦'.format(shopcart.goodinfo.name)
                        raise StockException(message)
                    orderdetail.count = shopcart.buy_num
                    orderdetail.total = float(shopcart.buy_num*shopcart.goodinfo.price)
                    orderdetail.save()
                    ordermain.total += orderdetail.total
                    ShopCart.objects.filter(pk=shopcart.pk).delete()
                if ordermain.total < 10:
                    ordermain.total += 10
                ordermain.save()
        except StockException as e:
            message = e
            return render(request,'shop_order/message.html',locals())
        return redirect(reverse('shoporder:my_order',kwargs={'order_id':ordermain.pk}))

# 添加购物车
class CartAppendGoodView(View):
    def get(self,request,gid):
        buy_num = request.GET.get('buy_num')
        if request.user.is_authenticated:
            shopcart,is_create = ShopCart.objects.update_or_create(user=request.user,goodinfo_id=gid)
            shopcart.buy_num = buy_num
            shopcart.save()
            goods_num = ShopCart.objects.filter(user=request.user,status=0).count()
        else:
            sessionid = request.COOKIES.get('mysessionid')
            shopcartcache = User_Cart_Cache()
            shopcartcache.cart_append_good_cache(sessionid,gid,buy_num)
            goods_num = shopcartcache.get_cart_len_cache(sessionid)
        return JsonResponse({
            'code':0,
            'goods_num':goods_num,
        })

# 删除购物车商品
class CartDeleteGoodView(View):
    def get(self,request,gid):
        if request.user.is_authenticated:
            ShopCart.objects.filter(user=request.user,goodinfo_id=gid).delete()
        else:
            sessionid = request.COOKIES.get('mysessionid')
            shopcartcache = User_Cart_Cache()
            shopcartcache.delete_goods_cache(sessionid,gid)
        return JsonResponse({'code':0})

# 修改购物车中商品数量
class CartUpdateGoodNumView(View):
    def get(self,request,gid):
        res = {'code':0}
        buy_num = int(request.GET.get('buy_num'))
        if buy_num:
            goods_info = GoodsInfo.objects.get(pk=gid)
            if goods_info.stock < buy_num:
                res['code'] = 1
                return JsonResponse(res)
            if request.user.is_authenticated:
                ShopCart.objects.filter(user=request.user,goodinfo_id=gid).update(buy_num=buy_num)
            else:
                shopcartcache = User_Cart_Cache()
                sessionid = request.COOKIES.get('mysessionid')
                shopcartcache.cart_append_good_cache(sessionid,gid,buy_num)
            res['buy_num'] = buy_num
        return JsonResponse(res)
