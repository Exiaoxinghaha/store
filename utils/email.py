# -*-coding:utf-8-*-
from django.core.mail import send_mail
from django.conf import settings
from account.models import EmailCode
import uuid

# 注册邮件
def RegisterEmail(user):
    email =EmailCode()
    email.user = user
    email.code = uuid.uuid4()
    email.email_type = 0
    email.save()
    email_title = '用户注册'
    html_message = '<a href = "http://192.168.43.107:8000/account/activate/?code={}">欢迎注册，点击此链接激活您的账号</a>'.format(email.code)
    send_mail(email_title,'',settings.EMAIL_FROM,[user.email],html_message=html_message)

# 忘记密码
def ForgetPasswordEmail(user):
    email = EmailCode()
    email.user = user
    email.code = uuid.uuid4()
    email.email_type = 1
    email.save()
    email_title = '修改密码'
    html_message = '<a href = "http://192.168.43.107:8000/account/modify_password/?code={}">申请成功!点击此链接进行修改</a>'.format(email.code)
    send_mail(email_title,'',settings.EMAIL_FROM,[user.email],html_message=html_message)