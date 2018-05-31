from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    receiver_default = models.ForeignKey('ReceiverAddress',related_name='user_receiver',null=True,default=None,verbose_name='默认收货地址')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username

class UserDetail(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=10,null=True)
    gender = models.CharField(max_length=10,null=True)
    city = models.CharField(max_length=10,null=True)
    telephone = models.CharField(max_length=11,null=True)
    address = models.CharField(max_length=50,null=True)

class EmailCode(models.Model):
    EMAIL_TYPE = (
        (0,'激活'),
        (1,'修改密码')
    )
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    code = models.CharField('验证码',max_length=40)
    create_time = models.DateField('创建时间',auto_now_add=True)
    email_type = models.SmallIntegerField('邮件类型',choices=EMAIL_TYPE)

class ReceiverAddress(models.Model):
    user = models.ForeignKey(UserProfile,related_name='receiver_user')
    receiver_city = models.CharField('收货人城市',max_length=10)
    receiver_telephone = models.CharField('收货人电话',max_length=11)
    receiver_address = models.CharField('收货地址',max_length=150)
    receiver_name = models.CharField('收货人姓名',max_length=10)
    status = models.SmallIntegerField('状态',default=0)

    class Meta:
        verbose_name = '收货人信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.receiver_name



