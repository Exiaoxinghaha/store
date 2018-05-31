from django.db import models
from account.models import UserProfile
from shop.models import GoodsInfo

class ShopCart(models.Model):
    STATUS = (
        (0,'正常'),
        (1,'删除'),
    )
    goodinfo = models.ForeignKey(GoodsInfo,verbose_name='商品信息',on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,verbose_name='所属用户',on_delete=models.CASCADE)
    buy_num = models.IntegerField(default=0,verbose_name='购买数量')
    create_time =models.DateField(auto_now=True)
    status = models.SmallIntegerField(choices=STATUS,default=0,verbose_name='购物车商品状态')

    class Meta:
        unique_together = ('goodinfo','user')
    def __str__(self):
        return self.user.username