"""webstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from account import views

urlpatterns = [
    url(r'^register/$',views.RegisterView.as_view(),name='register'),
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    url(r'^activate/$',views.Activate.as_view(),name='activate'),
    url(r'^logout/$',views.LoginOut.as_view(),name='logout'),
    url(r'^check_username/$',views.Check_Username.as_view(),name='check_username'),
    url(r'^modify_password/$',views.ModifyPassword.as_view(),name='modify_password'),
    url(r'^forget_password/$',views.Forgetpassword.as_view(),name='forget_password'),
    url(r'^only_modify_pwd/$',views.OnlyModifyPwd.as_view(),name='only_modify_pwd'),
    url(r'^user_center_info/$',views.UserCenterInfo.as_view(),name='user_center_info'),
    url(r'^edit_user_info/$',views.EditUserInfo.as_view(),name='edit_user_info'),
    url(r'^user_center_site/$',views.UserCenterSite.as_view(),name='user_center_site'),
    url(r'^set_default_site/$',views.SetDefaultSite.as_view(),name='set_default_site'),
    url(r'^del_receiver_site/$',views.DelReceiverSite.as_view(),name='del_receiver_site'),
    url(r'^edit_receiver_ajax/$',views.EditReceiverAjax.as_view(),name='edit_receiver_ajax'),
    url(r'^modify_receiver_address/$',views.ModifyReceiverAddress.as_view(),name='modify_receiver_address'),
    url(r'^edit_user_info_ajax/$',views.EditUserInfoAjax.as_view(),name='edit_user_info_ajax'),
    url(r'^user_center_order/$',views.UserCenterOrder.as_view(),name='user_center_order'),
]
