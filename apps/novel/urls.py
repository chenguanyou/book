from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name="index" ), #首页url视图
    url(r'^tege/$', TageView.as_view(), name="noveltage"), #用于小说分类的url视图
    url(r'^book/(?P<book_id>\d+)/$', BookDetailsView.as_view(), name="book"), #用于小说的详情视图处理
    url(r'^text/(?P<text_id>\d+)/$', TextView.as_view(), name="text"), #用于小说内容的视图处理
    url(r'addfave/$', BookDetailsView.as_view(), name="addfave"),  # 用于把小说加入收藏处理
    url(r'PingView/$', PingView.as_view(), name="pingview"), #小说详情的评论加载 ---> 这个功能还没有完成
    url(r'search/$', SearchView.as_view(), name="search"), #小说的全局搜索url
]