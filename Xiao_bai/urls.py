"""Xiao_bai URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
import xadmin

from novel import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),  # 首页url视图
    url(r'^admin/', include(xadmin.site.urls)), #后台url视图
    url(r'^users/', include('users.urls', namespace="users")), #用户中心相关的url视图
    url(r'^captcha/', include('captcha.urls')), #生成验证码
    url(r'^novel/', include('novel.urls', namespace = "novel")), #小说相关的url视图
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #图片的url连接
