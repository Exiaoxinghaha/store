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
from django.conf.urls import url,include
from django.contrib import admin
from shop import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view()),
    url(r'tinymce/', include('tinymce.urls')),
    url(r'^search/',include('haystack.urls')),
    url(r'^check_code/$', views.Check_Code, name='check_code'),
    url(r'^account/',include('account.urls',namespace='account')),
    url(r'^shop/',include('shop.urls',namespace='shop')),
    url(r'^shopcart/',include('shopcart.urls',namespace='shopcart')),
    url(r'^shoporder/',include('shoporder.urls',namespace='shoporder')),
]

handler404 = views.Page_Not_Found
handler500 = views.Server_Error

