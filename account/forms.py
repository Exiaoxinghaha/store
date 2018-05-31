# -*-coding:utf-8-*-
from django import forms

# 注册
class RegisterFrom(forms.Form):
    username = forms.CharField(min_length=5,max_length=20,required=True)
    password1 = forms.CharField(min_length=8,max_length=20,required=True)
    password2 = forms.CharField(min_length=8,max_length=20,required=True)
    verify_code = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    allow = forms.CharField(required=True)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次密码不一致',code=password2)
        return password2

# 登录
class LoginForm(forms.Form):
    username = forms.CharField(min_length=5,max_length=20,required=True)
    password = forms.CharField(min_length=8,max_length=20,required=True)

# 忘记密码
class ForgetPwdForm(forms.Form):
    username = forms.CharField(min_length=5,max_length=20,required=True)

# 修改密码
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(min_length=8,max_length=20,required=True)
    password2 = forms.CharField(min_length=8,max_length=20,required=True)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次密码不一致',code=password2)
        return password2

# 修改密码
class OnlyModifyForm(forms.Form):
    username = forms.CharField(min_length=5,max_length=20,required=True)
    password1 = forms.CharField(min_length=8,max_length=20,required=True)
    password2 = forms.CharField(min_length=8,max_length=20,required=True)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次次新密码不一致',code=password2)
        return password2

# 编辑个人信息
class EditUserInfoForm(forms.Form):
    telephone = forms.CharField(min_length=11,max_length=11,required=False)
    address = forms.CharField(max_length=50,required=False)
    city = forms.CharField(max_length=10,required=False)
    gender = forms.CharField(max_length=10,required=False)

# 收货地址
class ReceiverAddressForm(forms.Form):
    receiver_name = forms.CharField(max_length=10,required=True)
    receiver_telephone = forms.CharField(min_length=11,max_length=11,required=True)
    receiver_city = forms.CharField(max_length=10)
    receiver_address = forms.CharField(max_length=150,required=True)

# 修改收货地址
class ModifyReceiverAddressForm(forms.Form):
    receiver_name1 = forms.CharField(max_length=10,required=True)
    receiver_telephone1 = forms.CharField(min_length=11,max_length=11,required=True)
    receiver_city1 = forms.CharField(max_length=10)
    receiver_address1 = forms.CharField(max_length=150,required=True)