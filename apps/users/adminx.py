import xadmin
from xadmin import views #引入xadmin的主题视图来支持主题选择

from .models import *



#让xadmin后台支持主题选择
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True



#修改xadmin的头部和底部信息
class GlobalSetting(object):
    site_title = "小白读书后台管理系统"
    site_footer = "小白读书网"
    menu_style = "accordion" #把App收缩起来



#普通用户管理注册
class UserProFileAdmin(object):
    list_display = ["hy_dj","gender","nick_name","email","mobile","hy_xbb","register_time"] #后台显示类型
    search_fields = ["hy_dj","gender","nick_name","email","mobile"] #设置搜索
    list_filter = ["hy_dj","gender","nick_name","email","mobile"] #搜索过滤器
    model_icon = "fa fa-user" #这样可以替换与设置原有的Xadmin的图标

    def queryset(self):  # 获取非管理员用户
        qs = super(UserProFileAdmin, self).queryset()
        qs = qs.filter(is_staff=0, sign_bool=False)
        return qs



# 管理员用户管理注册
class AdminProAdmin(object):
    list_display = ["hy_dj", "gender", "nick_name", "email", "mobile", "hy_xbb", "register_time"]  # 后台显示类型
    search_fields = ["hy_dj", "gender", "nick_name", "email", "mobile"]  # 设置搜索
    list_filter = ["hy_dj", "gender", "nick_name", "email", "mobile"]  # 搜索过滤器
    model_icon = "fa fa-user"  # 这样可以替换与设置原有的Xadmin的图标

    def queryset(self):  # 获取管理员用户
        qs = super(AdminProAdmin, self).queryset()
        qs = qs.filter(is_staff=1)
        return qs



# 签约作者的管理注册
class SingUserAdmin(object):
    list_display = ["hy_dj", "sign_bool", "gender", "nick_name", "email", "mobile", "hy_xbb", "register_time"]  # 后台显示类型
    search_fields = ["hy_dj", "gender", "nick_name", "email", "mobile"]  # 设置搜索
    list_filter = ["hy_dj", "gender", "nick_name", "email", "mobile"]  # 搜索过滤器
    model_icon = "fa fa-user"  # 这样可以替换与设置原有的Xadmin的图标

    def queryset(self):  # 获取管理员用户
        qs = super(SingUserAdmin, self).queryset()
        qs = qs.filter(sign_bool=True)
        return qs



#充值记录验证码注册
class RechargeUserAdmin(object):
    list_display = ["user_name","RechargeSum","RechargeRecord"] #后台显示类型
    search_fields = ["user_name","RechargeSum"] #设置搜索
    list_filter = ["user_name","RechargeSum","RechargeRecord"] #搜索过滤器
    model_icon = "fa fa-credit-card" #这样可以替换与设置原有的Xadmin的图标



#邮箱验证码注册
class EmailVerifyRecordAdmin(object):
    list_display = ["code","email","send_type","send_time"] #后台显示类型
    search_fields = ["code","email","send_type"] #设置搜索
    list_filter = ["code","email","send_type","send_time"] #搜索过滤器
    model_icon = "fa fa-envelope" #这样可以替换与设置原有的Xadmin的图标


# #用户的小说收藏记录
# class CollectionAdmin(object):
#     list_display = ["user_name","novel_name","novel_time"] #后台显示类型
#     search_fields = ["user_name","novel_name"] #设置搜索
#     list_filter = ["user_name","novel_name"] #搜索过滤器
#     model_icon = "fa fa-star" #这样可以替换与设置原有的Xadmin的图标


# #用户的作者收藏记录
# class AuthorAdmin(object):
#     list_display = ["user_name","novel_name","novel_time"] #后台显示类型
#     search_fields = ["user_name","novel_name"] #设置搜索
#     list_filter = ["user_name","novel_name"] #搜索过滤器
#     model_icon = "fa fa-heart" #这样可以替换与设置原有的Xadmin的图标
#
#
# #用户的小说阅读记录
# class ReadNovelAdmin(object):
#     list_display = ["user_name","novel_name","novel_time"] #后台显示类型
#     search_fields = ["user_name","novel_name"] #设置搜索
#     list_filter = ["user_name","novel_name"] #搜索过滤器
#     model_icon = "fa fa-book" #这样可以替换与设置原有的Xadmin的图标


#用户的消息记录注册
class MessagesAdmin(object):
    list_display = ["user_name","mess_title","mess_text","mess_time"] #后台显示类型
    search_fields = ["user_name","mess_title","mess_text"] #设置搜索
    list_filter = ["user_name","mess_title","mess_text"] #搜索过滤器
    model_icon = "fa fa-comments" #这样可以替换与设置原有的Xadmin的图标



#用户的评论管理注册
class CommentModelsAdmin(object):
    list_display = ["user_id","book_id","commtitle","comment","comment_data"] #后台显示类型
    search_fields = ["user_id","book_id","commtitle","comment"] #设置搜索
    list_filter = ["user_id","book_id","commtitle","comment"] #搜索过滤器
    model_icon = "fa fa-coffee" #这样可以替换与设置原有的Xadmin的图标




xadmin.site.unregister(UserProFile) #先卸载自动注册的后台用户管理，在重新注册
xadmin.site.register(UserProFile, UserProFileAdmin) #注册用户的管理
xadmin.site.register(SingUser, SingUserAdmin) #注册签约作者的管理
xadmin.site.register(AdminPro, AdminProAdmin) #管理员管理
xadmin.site.register(RechargeUser, RechargeUserAdmin) #注册用户的充值记录
xadmin.site.register(Messages, MessagesAdmin) #注册用户中心的系统消息到后台
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin) #注册后台用户的邮件发送记录
# xadmin.site.register(Collection, CollectionAdmin) #注册后台用户的小说收藏记录
# xadmin.site.register(Author, AuthorAdmin) #注册后台用户的作者收藏记录
# xadmin.site.register(ReadNovel, ReadNovelAdmin) #注册后台用户的小说阅读记录
xadmin.site.register(views.BaseAdminView, BaseSetting) #注册xadmin的主题视图来支持主题选择
xadmin.site.register(views.CommAdminView, GlobalSetting) #注册修改xadmin后台的页头和底部信息
xadmin.site.register(CommentModels, CommentModelsAdmin) #注册用户的评论