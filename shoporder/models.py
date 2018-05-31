from django.db import models
from account.models import UserProfile,ReceiverAddress
from shop.models import GoodsInfo

# 订单中心
class OrderMain(models.Model):
    order_status = (
        (-1,'取消'),
        (0,'创建'),
        (1,'未支付'),
        (2,'已支付'),
        (3,'未发货'),
        (4,'已发货')
    )
    order_number = models.CharField(max_length=50,unique=True,verbose_name='订单编号')
    sub_time = models.DateField(auto_now_add=True,verbose_name='提交时间')
    pay_time = models.DateField(null=True,blank=True,verbose_name='付款时间')
    status = models.SmallIntegerField(choices=order_status,default=0,verbose_name='订单状态')
    total = models.DecimalField(null=True,max_digits=10,decimal_places=2,verbose_name='商品总价')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name='用户')
    receiver = models.ForeignKey(ReceiverAddress,on_delete=models.CASCADE,default=None,null=True,verbose_name='收货地址')

    class Meta:
        verbose_name = '订单中心'
        verbose_name_plural = verbose_name
        ordering = ('-id',)
    def __str__(self):
        return str(self.user)+str(self.id)

# 订单详情
class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain,verbose_name='订单中心')
    goods_info = models.ForeignKey(GoodsInfo,verbose_name='商品信息')
    goods_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    total = models.DecimalField(null=True,default=0,max_digits=10,decimal_places=2,verbose_name='商品总价')
    # 这个count名字起的不好，应该用buy_num
    count = models.IntegerField(verbose_name='商品数量')

    class Meta:
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name
        ordering = ('-id',)
    def __str__(self):
        return str(self.order)+str(self.goods_info.id)

