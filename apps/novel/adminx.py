import xadmin

from .models import *


'''在小说里面直接添加章节'''
class NovelChaPterInlines(object):
    model = NovelChaPter
    extra = 0


'''注册小说的频道'''
class ChannelViewAdmin(object):
    list_display = ["channel_name"] #后台显示类型
    search_fields = ["channel_name"] #设置搜索
    list_filter = ["channel_name"] #搜索过滤器
    model_icon = "fa fa-bar-chart" #这样可以替换与设置原有的Xadmin的图标


'''小说的类别管理'''
class TagModelViewAdmin(object):
    list_display = ["tag_id","tag_name"] #后台显示类型
    search_fields = ["tag_id","tag_name"] #设置搜索
    list_filter = ["tag_id","tag_name"] #搜索过滤器
    model_icon = "fa fa-bookmark" #这样可以替换与设置原有的Xadmin的图标



'''注册小说管理'''
class NovelModelViewAdmin(object):
    list_display = ["novel_name","novel_tag","novel_user","novel_byte","novel_read","novel_time"] #后台显示类型
    search_fields = ["novel_name","novel_user","novel_byte","novel_read"] #设置搜索
    list_filter = ["novel_name","novel_user","novel_byte","novel_read"] #搜索过滤器
    model_icon = "fa fa-file-archive-o" #这样可以替换与设置原有的Xadmin的图标
    inlines = [NovelChaPterInlines,] #在inlines里面添加章节编辑添加


'''注册小说的广告管理'''
class IndexNovelAdmin(object):
    list_display = ["title","novel","novel_image","addtime"] #后台显示类型
    search_fields = ["title","novel","novel_image"] #设置搜索
    list_filter = ["title","novel","novel_image"] #搜索过滤器
    model_icon = "fa fa-retweet" #这样可以替换与设置原有的Xadmin的图标



'''注册小说的章节管理'''
class NovelChaPterViewAdmin(object):
    list_display = ["novelchapter_cover","novelchapter_name","novelchapter_time"] #后台显示类型
    search_fields = ["novelchapter_cover","novelchapter_name","novelchapter_text"] #设置搜索
    list_filter = ["novelchapter_cover","novelchapter_name","novelchapter_text"] #搜索过滤器
    model_icon = "fa fa-file-text" #这样可以替换与设置原有的Xadmin的图标



'''注册小说的广告管理'''
class IndexAdViewAdmin(object):
    list_display = ["adTitle","adText","adUrl","addtime"] #后台显示类型
    search_fields = ["adTitle","adText","adUrl"] #设置搜索
    list_filter = ["adTitle","adText","adUrl"] #搜索过滤器
    model_icon = "fa fa-plus-square" #这样可以替换与设置原有的Xadmin的图标


xadmin.site.register(Channel, ChannelViewAdmin) #注册小说的频道
xadmin.site.register(TagModel, TagModelViewAdmin) #注册小说的分类管理
xadmin.site.register(IndexNovel,IndexNovelAdmin) #注册小说的首页数据推荐
xadmin.site.register(NovelModel, NovelModelViewAdmin) #注册小说的管理
xadmin.site.register(NovelChaPter, NovelChaPterViewAdmin) #注册小说的章节管理器
xadmin.site.register(IndexAdView, IndexAdViewAdmin) #小说的首页广告管理

