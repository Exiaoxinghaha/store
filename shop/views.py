from django.shortcuts import render,HttpResponse
from io import BytesIO
from utils.verification import verification_pic
from django.views import View
from django.db.models import F
from .models import GoodsInfo,GoodsArea,GoodsCategory
from shop.cache import User_Browse_History_Cache

class IndexView(View):
    def get(self,request):
        goods_list = []
        categorys = GoodsCategory.objects.filter(status=0).all()
        for category in categorys:
            goodsinfos = GoodsInfo.objects.filter(category=category).all()[:4]
            goods_list.append({
                "category":category,
                "goodsinfos":goodsinfos
            })
        return render(request,'shop/index.html',locals())

# 图片验证码视图
def Check_Code(request):
    stream = BytesIO()
    image,code = verification_pic()
    image.save(stream,'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

# 商品列表视图
class CategroysView(View):
    def get(self,request,cid):
        order_by = request.GET.get('order_by','id')
        if order_by == 'click_count':
            order_by = '-click_count'
        goods_list = GoodsInfo.objects.filter(category_id=cid).order_by(order_by)[:5]
        goods_categroy = GoodsCategory.objects.filter(pk=cid).first
        return render(request,'shop/list.html',locals())

# 商品详情视图
class GoodsDetailView(View):
    def get(self,request,gid):
        goods_info = GoodsInfo.objects.filter(pk=gid).first()
        browse_history = User_Browse_History_Cache()
        if request.user.is_authenticated:
            browse_history.add_cache(request.user.id,gid)
        else:
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                key = request.META['HTTP_X_FORWARDED_FOR']
            else:
                key = request.META['REMOTE_ADDR']
            browse_history.add_cache(key,gid)
        GoodsInfo.objects.filter(pk=gid).update(click_count=F('click_count')+1)
        return render(request,'shop/detail.html',locals())

# 404页面
def Page_Not_Found(request):
    return render(request,'404.html')
# 500页面
def Server_Error(request):
    return render(request,'500.html')