from django.db import models
from tinymce.models import HTMLField

# 商品分类
class GoodsCategory(models.Model):
    STATUS = (
        (0,'正常'),
        (1,'删除'),
    )
    name = models.CharField(max_length=20,verbose_name='商品分类名')
    status = models.SmallIntegerField(choices=STATUS,default=0,verbose_name='状态')

    class Meta:
        verbose_name_plural = '种类列表'
        verbose_name = '商品种类'
    def __str__(self):
        return self.name

# 商品产地
class GoodsArea(models.Model):
    name = models.CharField(max_length=20,verbose_name='产地名')

    class Meta:
        verbose_name_plural = '产地列表'
        verbose_name = '商品产地'
    def __str__(self):
        return self.name

# 商品详情
class GoodsInfo(models.Model):
    STATUS = (
        (0,'正常'),
        (1,'删除'),
    )
    name = models.CharField(max_length=30,verbose_name='商品名称')
    images = models.ImageField(upload_to='goods/%Y/%m/%d',verbose_name='商品图片地址')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    click_count = models.IntegerField(default=0,verbose_name='商品点击量')
    unit = models.CharField(max_length=10,verbose_name='单位')
    status = models.SmallIntegerField(choices=STATUS,default=0,verbose_name='状态')
    description = models.TextField(verbose_name='商品描述')
    stock = models.IntegerField(verbose_name='商品库存')
    detail = HTMLField(verbose_name='商品详情')
    category = models.ForeignKey(GoodsCategory,verbose_name='商品分类')
    area = models.ForeignKey(GoodsArea,verbose_name='商品产地',null=True)

    class Meta:
        verbose_name = '商品详情'
        verbose_name_plural = '商品列表'

    def __str__(self):
        return self.name