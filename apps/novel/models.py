from datetime import datetime

from django.db import models

# Create your models here.
from users.models import UserProFile
from taggit.managers import TaggableManager


'''小说的标签管理'''
class Tage(models.Model):
    tag_name = TaggableManager()

    class Meta:
        verbose_name = "添加标签"
        verbose_name_plural = verbose_name



'''小说的频道'''
class Channel(models.Model):
    channel_name = models.CharField(max_length=20, default="", verbose_name="小说的频道")

    class Meta:
        verbose_name = "频道管理"
        verbose_name_plural = verbose_name
        db_table = "Channel"

    def __str__(self):
        return self.channel_name

    '''获取小说的所有类别'''
    def get_tag(self):
        return self.tagmodel_set.all().order_by("id")[:12]




'''小说的类别'''
class TagModel(models.Model):
    tag_id = models.ForeignKey(Channel, verbose_name="小说的频道")
    tag_name = models.CharField(max_length=20, verbose_name="小说的类别")

    class Meta:
        verbose_name = "类别管理"
        verbose_name_plural = verbose_name
        db_table = "TagModel"

    def __str__(self):
        return self.tag_name


'''小说的封面信息'''
class NovelModel(models.Model):
    novel_name = models.CharField(max_length=30, null=True, blank=True, verbose_name="小说的名称")
    novel_alias = models.CharField(max_length=30, default="", null=True, blank=True, verbose_name="小说的别名")
    novel_image = models.ImageField(upload_to="novel/%Y/%m", null=True, blank=True, max_length=100, verbose_name="小说的封面图")
    novel_user = models.ForeignKey(UserProFile, null=True, blank=True, verbose_name="小说的作者")
    novel_byte = models.IntegerField(default=0,  verbose_name="字节数")
    novel_read = models.IntegerField(default=0,  verbose_name="阅读量")
    novel_comment = models.IntegerField(default=0, verbose_name="评论量")
    novel_tag = models.ForeignKey(TagModel, null=True, blank=True, verbose_name="小说的类别")
    novel_Recommend = models.BooleanField(default=False,  verbose_name="是否幻灯片推荐")
    novel_tage = TaggableManager(verbose_name="标签选择")
    novel_text = models.TextField(max_length=200, null=True, blank=True, verbose_name="小说的简介")
    novel_fave = models.IntegerField(default=0, verbose_name="小说的收藏数")
    novel_next = models.IntegerField(default=0, verbose_name="浏览量")
    is_long = models.BooleanField(default=True, verbose_name="是否登录可读")
    novel_time = models.DateTimeField(default=datetime.now, verbose_name="小说更新时间")

    class Meta:
        verbose_name = "小说管理"
        verbose_name_plural = verbose_name
        db_table = "NovelModel"

    def __str__(self):
        return self.novel_name

    '''获取小说的章节'''
    def get_book(self):
        return self.novelchapter_set.all()

    '''获取小说最新的章节'''
    def get_time_book(self):
        return self.novelchapter_set.all().order_by("-id")[:1]

    '''获取小说第一章节'''
    def get_book_to(self):
        return self.novelchapter_set.all().order_by("id")[:1]

    # '''获取首页幻灯片横向图片的小说推广展示'''
    # def get_book_h(self):
    #     return self.indexnovel_set.all().order_by("-addtime")[:2]




'''小说的章节信息'''
class NovelChaPter(models.Model):
    novelchapter_cover = models.ForeignKey(NovelModel, verbose_name="所属小说")
    novelchapter_name = models.CharField(max_length=30, verbose_name="章节名称")
    novelchapter_text = models.TextField(verbose_name='章节内容')
    novelchapter_num = models.IntegerField(default=0, verbose_name="章节数")
    novelchapter_time = models.DateTimeField(default=datetime.now, verbose_name="章节更新时间")

    class Meta:
        verbose_name = "章节管理"
        verbose_name_plural = verbose_name
        db_table = "NovelChaPter"

    def __str__(self):
        return self.novelchapter_name



'''首页幻灯片里面的小说展示'''
class IndexNovel(models.Model):
    title = models.CharField(default="", max_length=10, verbose_name="推荐的小说标题")
    novel = models.ForeignKey(NovelModel, verbose_name="推荐的小说")
    novel_image = models.ImageField(upload_to="tuiimg/%Y/%m", null=True, blank=True, max_length=100,verbose_name="推荐小说的封面图")
    addtime = models.DateField(default=datetime.now, verbose_name="推荐时间")

    class Meta:
        verbose_name = "小说展示"
        verbose_name_plural = verbose_name
        db_table = "IndexNovel"

    def __str__(self):
        return self.title



'''首页视图的广告'''
class IndexAdView(models.Model):
    adTitle = models.CharField(max_length=20, default="", verbose_name="广告标题")
    adImage = models.ImageField(upload_to="addimg/%Y/%m", null=True, blank=True, max_length=100,verbose_name="小说的封面图")
    adText = models.CharField(max_length=100, default="", verbose_name="广告简介")
    adUrl = models.URLField(max_length=100, default="", verbose_name="广告url")
    addtime = models.TimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "广告管理"
        verbose_name_plural = verbose_name
        db_table = "IndexAdView"

    def __str__(self):
        return self.adTitle

