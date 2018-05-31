from django.shortcuts import render,redirect,reverse
from django.views import View
from account.models import EmailCode,UserProfile,UserDetail,ReceiverAddress
from utils.email import RegisterEmail,ForgetPasswordEmail
from account.forms import RegisterFrom,LoginForm,ForgetPwdForm,ModifyPwdForm,OnlyModifyForm,EditUserInfoForm,ReceiverAddressForm,ModifyReceiverAddressForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction
from shop.models import GoodsInfo
from shop.cache import User_Browse_History_Cache
from shoporder.models import OrderDetail,OrderMain

# 注册
class RegisterView(View):
    def get(self,request):
        return render(request,'account/register.html')
    def post(self,request):
        register_form = RegisterFrom(request.POST)
        if not register_form.is_valid():
            err_allow = '验证失败，请重新提交'
            return render(request,'account/register.html',locals())
        username = register_form.cleaned_data['username']
        user = UserProfile.objects.filter(username=username)
        if user:
            err_allow = '该用户已存在'
            return render(request,'account/register.html',locals())
        code = register_form.cleaned_data['verify_code']
        if not code == request.session['CheckCode']:
            err_allow = '验证码错误'
            return render(request, 'account/register.html', locals())
        with transaction.atomic():
            user = UserProfile()
            user.username = username
            user.password = make_password(register_form.cleaned_data['password2'])
            user.email = register_form.cleaned_data['email']
            user.is_active = False
            user.save()
            RegisterEmail(user)
        return render(request,'account/send_success.html')

# ajax验证用户是否存在
class Check_Username(View):
    def get(self,request):
        username = request.GET.get('username')
        count = UserProfile.objects.filter(username=username).count()
        return JsonResponse({'count':count})

# 激活
class Activate(View):
    def get(self,request):
        code = request.GET.get('code')
        email = EmailCode.objects.get(code=code)
        email.user.is_active = True
        email.user.save()
        return redirect(reverse('account:login'))

# 登录
class LoginView(View):
    def get(self,request):
        return render(request,'account/login.html')
    def post(self,request):
        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            err = '您的输入没有通过验证，请输入正确的信息再登录'
            return render(request,'account/login.html',locals())
        # username = login_form.cleaned_data['username']
        # user = UserProfile.objects.filter(username=username)
        user = authenticate(**login_form.cleaned_data)
        if not user:
            err = '用户名或密码错误'
            return render(request,'account/login.html',locals())
        login(request,user)
        return redirect(reverse('shop:index'))

# 注销
class LoginOut(View):
    def get(self,request):
        logout(request)
        return redirect('/')

# 修改密码/点击修改密码后使用
class ModifyPassword(View):
    def get(self,request):
        code = request.GET.get('code')
        return render(request,'account/reset_password.html',locals())
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if not modify_form.is_valid():
            return render(request,'account/reset_password.html')
        code = request.POST.get('code')
        email = EmailCode.objects.get(code=code)
        password = make_password(modify_form.cleaned_data['password2'])
        email.user.password = password
        email.user.save()
        return redirect(reverse('account:login'))

# 忘记密码
class Forgetpassword(View):
    def get(self,request):
        return render(request,'account/forget_password.html')
    def post(self,request):
        forget_form = ForgetPwdForm(request.POST)
        if not forget_form.is_valid():
            message = '用户名格式错误'
            return render(request,'account/forget_password.html',locals())
        username = forget_form.cleaned_data['username']
        user = UserProfile.objects.filter(username=username).first()
        if not user:
            message = '该用户不存在'
            return render(request,'account/forget_password.html',locals())
        ForgetPasswordEmail(user)
        return render(request,'account/send_success.html')

# 直接修改密码
class OnlyModifyPwd(View):
    def get(self,request):
        return render(request,'account/modify_password.html')
    def post(self,request):
        modify_form = OnlyModifyForm(request.POST)
        if not modify_form.is_valid():
            error = '你的信息填写有误!'
            return render(request,'account/modify_password.html',locals())
        username = modify_form.cleaned_data['username']
        password2 = modify_form.cleaned_data['password1']
        user = UserProfile.objects.filter(username=username).first()
        if not user:
            error = '该用户不存在'
            return render(request,'account/modify_password.html',locals())
        user.password = make_password(password2)
        user.save()
        return redirect(reverse('account:login'))

# 用户中心
class UserCenterInfo(LoginRequiredMixin,View):
    def get(self,request):
        id_list = []
        goods_info = []
        userdetail = UserDetail.objects.filter(user=request.user).first()
        browse_history = User_Browse_History_Cache()
        # 获取浏览记录中的商品id(缓存中的id为二进制类型使用时需要转换成int类型)
        good_id_list = browse_history.show_cache(request.user.id)
        # 去重
        for id in good_id_list:
            if int(id) not in id_list:
                id_list.append(int(id))
        for gid in id_list[:10]:
            goods = GoodsInfo.objects.filter(pk=gid).first()
            goods_info.append(goods)
        return render(request,'account/user_center_info.html',locals())

# 编辑个人信息
class EditUserInfo(LoginRequiredMixin,View):
    def post(self,request):
        edit_user_form = EditUserInfoForm(request.POST)
        if not edit_user_form.is_valid():
            return JsonResponse({'status':1})
        userdetail = UserDetail.objects.get(user=request.user)
        userdetail.gender = edit_user_form.cleaned_data['gender']
        userdetail.city = edit_user_form.cleaned_data['city']
        userdetail.telephone = edit_user_form.cleaned_data['telephone']
        userdetail.address = edit_user_form.cleaned_data['address']
        userdetail.save()
        return JsonResponse({'status':0})

# 个人信息ajax
class EditUserInfoAjax(View):
    def get(self,request):
        user = UserDetail.objects.get(user=request.user)
        print(user)
        return JsonResponse({
            'name':request.user.username,
            'city':user.city,
            'telephone':user.telephone,
            'address':user.address,
            'gender':user.gender,
        })


# 添加收货地址
class UserCenterSite(LoginRequiredMixin,View):
    def get(self,request):
        receiver_infos = ReceiverAddress.objects.filter(user=request.user,status=0).all()
        user = UserProfile.objects.get(pk=request.user.id)
        return render(request,'account/user_center_site.html',locals())
    def post(self,request):
        receiver_form = ReceiverAddressForm(request.POST)
        if not receiver_form.is_valid():
           return JsonResponse({'status':1})
        receiver = ReceiverAddress(**receiver_form.cleaned_data)
        receiver.user = request.user
        receiver.save()
        return JsonResponse({'status':0})

# 设置默认地址
class SetDefaultSite(LoginRequiredMixin,View):
    def get(self,request):
        data_id = request.GET.get('data_id')
        user = UserProfile.objects.get(pk=request.user.id)
        user.receiver_default_id = data_id
        user.save()
        return JsonResponse({
            'status': 0,
            'receiver_name': user.receiver_default.receiver_name,
            'receiver_city': user.receiver_default.receiver_city,
            'receiver_address': user.receiver_default.receiver_address,
            'receiver_telephone': user.receiver_default.receiver_telephone,
        })

# 删除收货地址
class DelReceiverSite(View):
    def get(self,request):
        data_id = int(request.GET.get('data_id'))
        is_default = 0
        user = UserProfile.objects.get(pk=request.user.id)
        if user.receiver_default_id == data_id:
            user.receiver_default_id = None
            user.save()
            is_default = 1
        # receiver = ReceiverAddress.objects.get(pk=data_id)
        # receiver.status = 1
        # receiver.save()
        ReceiverAddress.objects.filter(pk=data_id).update(status=1)
        return JsonResponse({'status':0,'is_default':is_default})

# 编辑收货地址的ajax请求
class EditReceiverAjax(View):
    def get(self,request):
        data_id = request.GET.get('data_id')
        receiver = ReceiverAddress.objects.get(pk=data_id)
        return JsonResponse({
            'receiver_name' : receiver.receiver_name,
            'receiver_city' : receiver.receiver_city,
            'receiver_address' : receiver.receiver_address,
            'receiver_telephone' : receiver.receiver_telephone,
        })

# 修改收货地址
class ModifyReceiverAddress(View):
    def post(self,request):
        receiver_form = ModifyReceiverAddressForm(request.POST)
        if not receiver_form.is_valid():
            return JsonResponse({'status':1})
        data_id = request.POST.get('data_id')
        receiver_name = receiver_form.cleaned_data['receiver_name1']
        receiver_city = receiver_form.cleaned_data['receiver_city1']
        receiver_address = receiver_form.cleaned_data['receiver_address1']
        receiver_telephone = receiver_form.cleaned_data['receiver_telephone1']
        ReceiverAddress.objects.filter(pk=data_id).update(receiver_name=receiver_name,receiver_city=receiver_city,receiver_telephone=receiver_telephone,receiver_address=receiver_address)
        return JsonResponse({'status':0})

# 订单中心
class UserCenterOrder(View):
    def get(self,request):
        order_info = []
        orders = OrderMain.objects.filter(user=request.user).all()
        for order in orders:
            order_details = OrderDetail.objects.filter(order=order).all()
            order_info.append({
                'order':order,
                'order_details':order_details
            })
        return render(request,'account/user_center_order.html',locals())