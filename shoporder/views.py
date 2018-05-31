from django.shortcuts import render,redirect,reverse
from django.views import View
from shoporder.models import OrderMain,OrderDetail
from account.models import UserProfile,ReceiverAddress
from django.db.models import F
from django.db import transaction
from utils.exception import StockException
from django.http import HttpResponseBadRequest,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# 订单中心
class UserOrderViews(LoginRequiredMixin,View):
    def get(self,request,order_id):
        order = OrderMain.objects.get(pk=order_id)
        orderdetails = OrderDetail.objects.filter(order=order).all()
        receiver = ReceiverAddress.objects.filter(pk=request.user.receiver_default_id).first()
        goods_num = len(orderdetails)
        return render(request,'shop_order/place_order.html',locals())
    def post(self,request,order_id):
        order = OrderMain.objects.get(pk=order_id)
        receiver_id = request.POST.get('receiver_id')
        order_details = OrderDetail.objects.filter(order=order).all()
        try:
            with transaction.atomic():
                for order_detail in order_details:
                    if order_detail.goods_info.stock < order_detail.count:
                        message = '{}库存不足哦'.format(order_detail.goods_info.name)
                        raise StockException(message)
                    order_detail.goods_info.stock = F('stock') - order_detail.count
                    order_detail.goods_info.save()
                order.receiver_id = receiver_id
                order.status = 1
                order.save()
        except StockException as e:
            order.status = -1
            order.save()
            message = e
            return render(request,'shop_order/message.html',locals())
        return redirect(reverse('account:user_center_order'))
# 取消订单
class CannelOrderViews(LoginRequiredMixin,View):
    def get(self,request):
        res = {'code':0}
        order_id = request.GET.get('order_id')
        order = OrderMain.objects.get(pk=order_id)
        if order.user != request.user:
            return HttpResponseBadRequest
        order_details = OrderDetail.objects.filter(order=order).all()
        with transaction.atomic():
            for order_detail in order_details:
                order_detail.goods_info.stock = F('stock')+order_detail.count
                order_detail.goods_info.save()
            order.status = -1
            order.save()
            return JsonResponse(res)
# 删除订单
class DeleteOrderViews(View):
    def get(self,request):
        order_id = request.GET.get('order_id')
        order = OrderMain.objects.get(pk=order_id)
        order_details = OrderDetail.objects.filter(order=order).all()
        try:
            for order_detail in order_details:
                order_detail.delete()
            order.delete()
        except Exception:
            return JsonResponse({'code':-1})
        return JsonResponse({'code':0})






