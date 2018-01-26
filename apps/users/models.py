from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser




# Create your models here.

'''用户表'''
class UserProFile(AbstractUser):
    nick_name = models.CharField(max_length=30, default="小白", verbose_name="昵称")
    sign_bool = models.BooleanField(default=False, verbose_name="签约")
    birday = models.DateField(null=True, blank=True, verbose_name="生日")
    address = models.CharField(max_length=200, verbose_name="地址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")
    is_jh = models.BooleanField(default=False, verbose_name="是否激活")
    hy_xbb = models.IntegerField(default=10, verbose_name="小白币")
    hy_dj = models.CharField(choices=(("pthy","普通会员"),("xbhy","小白会员"),("cjxb","超级小白")), default="pthy", max_length=10, verbose_name="会员等级")
    image = models.ImageField(upload_to="image/%Y/%m", default="image/default.png", null=True, blank=True, max_length=100, verbose_name="头像")
    gender = models.CharField(max_length=25, choices=(("male","男"),("female","女")), default="female", verbose_name="性别")
    register_time = models.DateTimeField(default=datetime.now, verbose_name="注册时间")

    class Meta:
        verbose_name = "普通用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


'''获取管理员用户'''
class AdminPro(UserProFile):

    class Meta:
        verbose_name = "管理信息"
        verbose_name_plural = verbose_name
        proxy = True #这里非常关键如果不设置会新建一个表

'''获取签约作者用户'''
class SingUser(UserProFile):

    class Meta:
        verbose_name = "签约作者"
        verbose_name_plural = verbose_name
        proxy = True #这里非常关键如果不设置会新建一个表

'''用户的消息中心'''
class Messages(models.Model):
    user_name = models.IntegerField(default=0, verbose_name="接收用户")
    mess_title = models.CharField(max_length=30, verbose_name="消息名称")
    mess_text = models.CharField(max_length=100, verbose_name="消息内容")
    mess_time = models.DateTimeField(default=datetime.now, verbose_name="消息发送时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name
        db_table = "Messages"


'''用户的充值记录'''
class RechargeUser(models.Model):
    user_name = models.CharField(max_length=20, verbose_name="用户名")
    user_id = models.IntegerField(default=0, verbose_name="用户ID")
    RechargeSum = models.IntegerField(default=0, verbose_name="充值金额")
    RechargeRecord = models.DateTimeField(default=datetime.now, verbose_name="充值记录")

    class Meta:
        verbose_name = "充值记录"
        verbose_name_plural = verbose_name
        db_table = "RechargeUser"


'''邮箱验证码表'''
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    is_sx = models.IntegerField(choices=(("1","可用"),("0","不可用"),), default="1", verbose_name="激活是否可以")
    send_type = models.CharField(max_length=20, choices=(("register","用户注册"), ("forget","找回密码"),("upload_email","修改邮箱")), default="register",verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name
        db_table = "EmailVerifyRecord"

    def __str__(self):
        return self.email

'''用户收藏过的小说'''
class Collection(models.Model):
    user_name = models.IntegerField(default=0, verbose_name="用户ID")
    novel_name = models.IntegerField(default=0, verbose_name="小说ID")
    novel_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏的小说"
        verbose_name_plural = verbose_name
        db_table = "Collections"



'''用户收藏的作者'''
class Author(models.Model):
    user_id = models.IntegerField(default=0, verbose_name="用户ID")
    user_name = models.CharField(max_length=20, verbose_name="用户名")
    novel_name = models.CharField(max_length=50, verbose_name="作者的名字")
    novel_id = models.IntegerField(verbose_name="作者的ID")
    novel_time = models.DateTimeField(default=datetime.now, verbose_name="收藏时间")

    class Meta:
        verbose_name = "收藏的作者"
        verbose_name_plural = verbose_name
        db_table = "Author"



'''用户阅读过的小说'''
class ReadNovel(models.Model):
    user_name = models.IntegerField(default=0, verbose_name="用户ID")
    novel_name = models.IntegerField(default=0, verbose_name="小说ID")
    chapter_num = models.IntegerField(default=0, verbose_name="小说的章节ID")
    novel_time = models.DateTimeField(default=datetime.now, verbose_name="阅读时间")

    class Meta:
        verbose_name = "阅读记录"
        verbose_name_plural = verbose_name
        db_table = "ReadNovel"



'''用户的评论'''
class CommentModels(models.Model):
    from novel.models import NovelModel
    user_id = models.ForeignKey(UserProFile, verbose_name="用户")
    book_id = models.ForeignKey(NovelModel, verbose_name="小说")
    commtitle = models.CharField(max_length=20, default="", verbose_name="评论标题")
    comment = models.CharField(max_length=200, verbose_name="评论内容")
    comment_data = models.DateTimeField(default=datetime.now, null=True, blank=True,verbose_name="评论时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name
        db_table = "CommentModels"

    def __str__(self):
        return self.comment
