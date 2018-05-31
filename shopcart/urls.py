from django.conf.urls import url
from shopcart import views

urlpatterns = [
    url(r'^my_cart/$',views.ShopCartView.as_view(),name='my_cart'),
    url(r'^cart_append_good/(?P<gid>\d*)/$',views.CartAppendGoodView.as_view(),name='cart_append_good'),
    url(r'^cart_delete_good/(?P<gid>\d*)/$',views.CartDeleteGoodView.as_view(),name='cart_delete_good'),
    url(r'^cart_update_good_num/(?P<gid>\d*)/$',views.CartUpdateGoodNumView.as_view(),name='cart_update_good_num'),
]