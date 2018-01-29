import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.hashers import make_password #在用户注册的时候加密用户的密码

from .forms import DlForm, ZcForm, UploadImageForm, MoforPwdForm, UploadinfoForm, CommentForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #用来加载分页器的异常
from util.mixin_utils import *
from .models import UserProFile, EmailVerifyRecord, Messages, Collection, ReadNovel
from util.email_send import *
from util.mixin_utils import LoginRequiredMIxin
from novel.models import NovelChaPter, NovelModel #用于收藏，通过章节表找到小说

# Create your views here.



'''用户的登陆响应'''
class IndexDlView(View):
    '''响应登陆页面'''
    def get(self, request):
        return render(request, 'login.html', locals())



    '''用于表单的登陆跳转'''
    def post(self, request):
        login_form = DlForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None: #判断用户名密码是否正确
                if user.is_jh: #判断用户是否激活
                    login(request, user)
                    return HttpResponseRedirect("/")
                    #return render(request, "user.html", locals())
                else:
                    return HttpResponse('{"messages":"jh", "jh":"用户名未激活"}', content_type='application/json')
            else:
                return HttpResponse('{"messages":"cw", "cw":"用户名密码错误"}', content_type='application/json')
        else:
            return render(request, "login.html", locals())




'''用户注销登录功能'''
class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")




'''用户的注册功能响应'''
class IndexZcView(View):
    def get(self, request):
        return render(request, "register.html", locals())

    def post(self, request):
        register_form = ZcForm(request.POST)
        if register_form.is_valid():
            #获取所有的注册的post数据
            usernames = request.POST.get("username", "")
            password = request.POST.get("password", "")
            password2 = request.POST.get("confirm_password", "")
            phone_number = request.POST.get("phone_number", "")
            email = request.POST.get("email", "")
            #来判断用户名，邮箱，手机号是否注册过, 以及用户名密码是否正确
            if UserProFile.objects.filter(username=usernames):
                return HttpResponse('{"messages":"cw", "cw":"用户名存在"}', content_type='application/json')
            if UserProFile.objects.filter(mobile=phone_number):
                return HttpResponse('{"messages":"cw", "cw":"手机号已经存在"}', content_type='application/json')
            if UserProFile.objects.filter(email=email):
                return HttpResponse('{"messages":"cw", "cw":"邮箱已经存在"}', content_type='application/json')
            if password == password2:
                new_user = UserProFile()
                new_user.nick_name = usernames
                new_user.password = make_password(password)
                new_user.mobile = phone_number
                new_user.email = email
                new_user.is_jh = False
                new_user.username = usernames
                new_user.save()
                #注册成功后给用户发送一个激活邮件
                send_register_email(email, "register", new_user.nick_name)
                #注册成功后给用户发送一个系统消息
                messages = Messages()
                messages.user_name = new_user.id
                messages.mess_title = "账号注册成功"
                messages.mess_text = "亲爱的%s,欢迎注册小白读书网会员，在这里和大家一起读书交流吧！" % new_user.nick_name
                messages.save()
                return render(request, "login.html", locals())
            else:
                return HttpResponse('{"messages":"cw", "cw":"您输入的密码不一致"}', content_type='application/json')
        return render(request, "register.html", locals())



'''用户激活响应'''
class ActiveUserView(View):
    def get(self, request, active_code):
        emails_code = EmailVerifyRecord.objects.filter(code=active_code)
        if emails_code:
            for email_code in emails_code:
                if email_code.is_sx:
                    #激活用户
                    user = UserProFile.objects.get(email=email_code.email)
                    user.is_jh = True
                    user.save()
                    #激活成功后给用户发送一个系统消息
                    message = Messages()
                    message.user_name = user.id
                    message.mess_title = "账号激活成功"
                    message.mess_text = "亲爱的%s,您的会员账号已经成功激活，接下来就尽情的乐吧！"%user.nick_name
                    message.save()
                    #把验证码设为失效
                    email_code.is_sx = False
                    email_code.save()
                    return render(request, "active.html")
                else:
                    return HttpResponse("链接不小心丢失了，还望阁下不要伤心...")
        else:
            return HttpResponse("链接不小心丢失了，还望阁下不要伤心...")



'''跳转用户中心的url'''
class UserView(LoginRequiredMIxin, View):
    def get(self, request):
        msg = "home"
        #通过用户的ID查找到对应的用户对象
        #为了省时间就直接复制了，很多地方都是可以封装的
        no_user = UserProFile.objects.get(id=request.user.id)
        #通过用户找到用户的作品，和作品的更新时间
        no_user_novel = NovelModel.objects.filter(novel_user=request.user.id).order_by("-novel_time")
        #为用户中心的用户作品添加作品分页的功能
        page = request.GET.get('page', 1)
        try:
            page = request.GET.get('page', 1)
            p = Paginator(no_user_novel, 3, request=request)
            num = p.page(page)
        except EmptyPage:
            page = 1
            num = p.page(page)
        except PageNotAnInteger:
            page = 1
            num = p.page(page)
        except:
            page = 1
            num = p.page(page)
        return render(request, "user.html", locals())



'''用户中心的设置视图'''
class UserSite(LoginRequiredMIxin, View):
    def get(self, request):
        msg = "site"
        return render(request, "updatePage.html", locals())
    '''修改用户中心的昵称等信息'''
    def post(self, request):
        user_info_form = UploadinfoForm(request.POST, instance=request.user)
        # print(user_info_form)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')



'''用户修改头像'''
class UploadImageView(LoginRequiredMIxin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"修改失败"}', content_type='application/json')


'''用户个人中心修改密码'''
class UpLoadPwdView(LoginRequiredMIxin,View):
    def post(self, request):
        mo_Pwd = MoforPwdForm(request.POST)
        if mo_Pwd.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不相等"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors ), content_type='application/json')



'''用户修改个人邮箱'''
class UpEmailView(LoginRequiredMIxin, View):
    def get(self, request):
        email = request.GET.get("email", "")
        if email:
            if UserProFile.objects.filter(email=email):
                return HttpResponse('{"email":"邮箱不可用"}', content_type='application/json')
            send_register_email(email, "upload_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')



'''验证更换邮箱的验证码和邮箱是否匹配'''
class UpEmailsView(LoginRequiredMIxin, View):
    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        if code and email:
            email_code = EmailVerifyRecord.objects.get(email=email, code=code, send_type="upload_email")
            if email_code and email_code.is_sx:
                user = request.user
                user.email = email
                user.save()
                email_code.is_sx = False
                email_code.save()
                email_upload(request.user.email, "OK")
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"email":"验证码失效"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码不能为空"}', content_type='application/json')



'''在个人中心显示我的消息'''
class UserMessage(LoginRequiredMIxin, View):
    def get(self, request):
        msg = "site"
        user_message = Messages.objects.filter(user_name=request.user.id).order_by("-mess_time")
        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
            p = Paginator(user_message, 4, request=request)
            message = p.page(page)
        except EmptyPage:
            page = 1
            message = p.page(page)
        except PageNotAnInteger:
            page = 1
            message = p.page(page)
        except:
            page = 1
            message = p.page(page)
        return render(request, "message.html", locals())



'''用户小说的收藏记录'''
class UserFave(LoginRequiredMIxin, View):
    #加载用户中心的收藏的响应
    def get(self, request):
        faves = Collection.objects.filter(user_name=request.user.id).order_by("-novel_time")
        fave = []
        for fav in faves:
            favee = NovelModel.objects.filter(id=int(fav.novel_name))
            for faved in favee:
                fave.append(faved)
        #判断是否有收藏数据
        if not fave:
            msg = "no"
        # 用户收藏列表的分页器功能
        try:
            page = request.GET.get('page', 1)
            p = Paginator(fave, 3, request=request)
            fave = p.page(page)
        except EmptyPage:
            page = 1
            fave = p.page(page)
        except PageNotAnInteger:
            page = 1
            fave = p.page(page)
        except:
            page = 1
            fave = p.page(page)
        return render(request, "bookShelf.html", locals())

    #用户收藏的删除
    def post(self, request):
        #获取要删除收藏的小说ID
        rem_id = request.POST.get("fav_id","")
        if rem_id:
            Collection.objects.filter(user_name=int(request.user.id), novel_name=int(rem_id)).delete()
            print("收藏小说删除成功@")
            #小说删除成功后让小说的收藏数-1
            novel = NovelModel.objects.get(id=rem_id)
            novel.novel_fave -= 1
            novel.save()
            return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')
        return render(request, "bookShelf.html", locals())



'''用户的小说阅读记录'''
class ReadTextView(LoginRequiredMIxin, View):
    def get(self, request):
        # 加载用户中心的阅读记录的响应
        faves = ReadNovel.objects.filter(user_name=request.user.id).order_by("-novel_time")
        fave = []
        for fav in faves:
            favee = NovelModel.objects.filter(id=int(fav.novel_name))
            for faved in favee:
                fave.append(faved)
        #判断用户是否有阅读数据
        if not fave:
            msg = "no"
        # 用户收藏列表的分页器功能
        try:
            page = request.GET.get('page', 1)
            p = Paginator(fave, 3, request=request)
            fave = p.page(page)
        except EmptyPage:
            page = 1
            fave = p.page(page)
        except PageNotAnInteger:
            page = 1
            fave = p.page(page)
        except:
            page = 1
            fave = p.page(page)
        return render(request, "render.html", locals())

    #清空用户的收藏记录
    def post(self, request):
        user_id = request.POST.get("fav_id","")
        if user_id:
            user_browse = ReadNovel.objects.filter(user_name=user_id)
            user_browse.delete()
            return render(request, "render.html", locals())




'''用户对小说的评论处理---这里这是添加评论'''
class CommentView(LoginRequiredMIxin, View):
    def post(self, request):
        com_from = CommentForm(request.POST)
        if com_from.is_valid():
            #评论数加一
            comment_num = NovelModel.objects.get(id=int(request.POST.get("book_id")))
            comment_num.novel_comment += 1
            comment_num.save()
            com_from.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')



'''当用户点击别的头像的时候跳转到当前对象的用户中心主页'''
class UserNoLogView(View):
    def get(self, request, nouser_id):
        #通过用户的ID查找到对应的用户对象
        no_user = UserProFile.objects.get(id=nouser_id)
        #通过用户找到用户的作品，和作品的更新时间
        no_user_novel = NovelModel.objects.filter(novel_user=nouser_id).order_by("-novel_time")
        #为用户中心的用户作品添加作品分页的功能
        page = request.GET.get('page', 1)
        try:
            page = request.GET.get('page', 1)
            p = Paginator(no_user_novel, 3, request=request)
            num = p.page(page)
        except EmptyPage:
            page = 1
            num = p.page(page)
        except PageNotAnInteger:
            page = 1
            num = p.page(page)
        except:
            page = 1
            num = p.page(page)
        #如果用户的requestID和对象的ID一致就跳转到当前用户自己的主页
        if request.user.id:
            if int(request.user.id) == int(nouser_id):
                msg = "home"
                return render(request, "user.html", locals())
        return render(request, "userhome.html", locals())




'''以下是写作中心的的视图响应处理'''

'''写作中心主页的视图'''#----还没有完成
class WritingHomeView(LoginRequiredMIxin, View):
    def get(self, request):
        user_book = NovelModel.objects.filter(novel_user=int(request.user.id))
        print(user_book)
        return render(request, "writing.html", locals())

    def post(self, request):
        print(request.POST)
        return render(request, "writing.html", locals())

