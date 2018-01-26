from django import forms
from .models import *

from captcha.fields import CaptchaField #验证码

#用户登陆验证
class DlForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required":"账号不能为空"})
    password = forms.CharField(required=True, min_length=5,error_messages={"required": "密码不能为空",})
   # captcha = CaptchaField(error_messages={"invalid":"验证码错误", "required":"验证码不能为空"}) #生成验证码

#用户的注册验证
class ZcForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required":"账号不能为空"})
    password = forms.CharField(required=True, max_length=32, min_length=8, error_messages={"required": "密码不能为空",})
    phone_number = forms.IntegerField(required=True, error_messages={"required": "手机号不能为空",})
    email = forms.EmailField(required=True, error_messages={"required":"邮箱不能为空"})


#用来修改用户中心的头像
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProFile
        fields = ['image']


#密码修改
class MoforPwdForm(forms.Form):
    password1 = forms.CharField(required=True, error_messages={"required": "密码不能为空"})
    password2 = forms.CharField(required=True, error_messages={"required": "密码不能为空"})


#用来修改用户中心的信息
class UploadinfoForm(forms.ModelForm):
    class Meta:
        model = UserProFile
        fields = ['nick_name','birday','gender','address','mobile']


#用来验证用户的评论内容
class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModels
        fields = ['user_id','book_id','commtitle','comment']