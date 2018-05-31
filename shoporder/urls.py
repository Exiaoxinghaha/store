# -*-coding:utf-8-*-
from django.conf.urls import url
from shoporder import views

urlpatterns = [
    url(r'^my_order/(?P<order_id>\d*)/$',views.UserOrderViews.as_view(),name='my_order'),
    url(r'^cannel_order/$',views.CannelOrderViews.as_view(),name='cannel_order'),
    url(r'^delete_order/$',views.DeleteOrderViews.as_view(),name='delete_order'),
]