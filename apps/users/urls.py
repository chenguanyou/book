from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^dl/$', IndexDlView.as_view(), name="dl"), #登陆的url视图处理
    url(r'^zc/$', IndexZcView.as_view(), name="zc"), #注册的url
    url(r'^out/$', LogoutView.as_view(), name="logout"), #用户退出
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(), name="active"), #用户账号激活
    url(r'^userhome/$', UserView.as_view(), name="userhome"), #用户的个人中心主页
    url(r'^usersite/$', UserSite.as_view(), name="usersiteup"), #用户中心的个人信息设置和POST请求请改昵称等信息
    url(r'^upimage/$', UploadImageView.as_view(), name="upimage"), #用户修改头像
    url(r'^uppassword/$', UpLoadPwdView.as_view(), name="uppassword"), #用户修改密码
    url(r'^upemail/$', UpEmailView.as_view(), name="upemail"), #给用户发送修改邮箱的验证码
    url(r'^upemails/$', UpEmailsView.as_view(), name="upemails"), #验证码邮箱和验证码是否匹配
    url(r'^message/$', UserMessage.as_view(), name="message"), #在用户中心显示当前用户的消息
    url(r'^userfave/$', UserFave.as_view(), name="userfave"), #用于处理用户的收藏url
    url(r'^userreader/$', ReadTextView.as_view(), name="userread"), #用于处理用户的浏览记录
    url(r'rest/$', ReadTextView.as_view(), name="rest"),  # 用于清除用户的小说的浏览记录
    url(r'^comment/$', CommentView.as_view(), name="comment"), #用于小说的评论
    url(r'^nouser/(?P<nouser_id>\d+)/$', UserNoLogView.as_view(), name="nouser"),  # 用于用户点击别的用户对象的时候跳转到别的用户中心响应视图
    url(r'^writing/$',WritingHomeView.as_view(), name="writinghome"), #用于作者的写作中心的主页视图


]