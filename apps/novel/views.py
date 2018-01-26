import time


from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db.models import Q #用于小说的搜索
from django.core import serializers #把数据转换成json数据


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #用来加载分页器的异常
# Create your views here.

from .models import *
from users.models import ReadNovel, Collection, CommentModels  # 导入小说阅读收藏模块



'''首页视图响应处理'''
class IndexView(View):
    def get(self, request):
        #获取频道
        channel = Channel.objects.all()[:2]
        #获取首页的广告
        indexId = IndexAdView.objects.all().order_by("-addtime")[:1]
        #获取首页推荐的小说
        novel_recomm = NovelModel.objects.filter(novel_Recommend=True).order_by("-id")[:2]
        novel_recomm_h = IndexNovel.objects.all().order_by("addtime")[:2]
        #首页的女生阅读量做多的小说
        woman_channer = Channel.objects.all()
        for channel_id in woman_channer:
            if channel_id.channel_name == "女生":
                woman_tag = TagModel.objects.filter(tag_id=channel_id)
                for tag in woman_tag:
                    woman_novel = NovelModel.objects.filter(novel_tag=tag.id).order_by("-id")[:6]
                    break
        #首页的火热专区---》按评论量来推荐
        fiery_novel = NovelModel.objects.all().order_by("-novel_comment")[:3]
        #首页的热门推荐 ---》按浏览量来推荐
        hot_novel = NovelModel.objects.all().order_by("-novel_next")[:6]
        #首页的编辑推荐 ---》按照最新的发布推荐
        now_novel = NovelModel.objects.all().order_by("-novel_time")[:6]
        return render(request, "index.html", locals())



'''小说的分类页面响应视图处理'''
class TageView(View):
    def get(self, request):
        try:
            #频道的赛选
            tag_id = request.GET.get("tagid",1) #获取首页传进来的频道ID
            channer_all = Channel.objects.all() #获取全部的频道
            cha = request.GET.get("cx", Channel.objects.get(id=tag_id).channel_name) #获取查询的值，如果没有就是获取频道的默认值
            tagmodel_all = TagModel.objects.filter(tag_id=(Channel.objects.get(channel_name=cha)))
            morenzhi = "" #小说频道的默认值
            for leibienum in tagmodel_all: #获取小说频道的默认值
                morenzhi = leibienum
                break
            #类别的赛选
            tag = request.GET.get("tag", str(morenzhi))
            tag_id = TagModel.objects.get(tag_name=(request.GET.get("tag", str(morenzhi))))
            if tag:
                novel_all = NovelModel.objects.filter(novel_tag=tag_id.id).order_by("-id")
                # 对分类选项列表进行分页
                try:
                    page = request.GET.get('page', 1)
                    p = Paginator(novel_all, 5, request=request)
                    novel_all = p.page(page)
                except:
                    page = 1
                    novel_all = p.page(page)
            #获取最后一个小说的更新时间
            novel_date = NovelModel.objects.order_by("id").last()
            return render(request, "centertag.html", locals())
        except:
            return render(request, "centertag.html", locals())




'''小说的详情页面识图处理'''
class BookDetailsView(View):
    def get(self, request, book_id):
        #获取今天的时间,用于判断小说的发布时间是否是今天
        datetimes = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        #获取所有小说用于小说推荐，并且按照阅读数排序
        book_all = NovelModel.objects.all().order_by("-novel_read")[:10]
        #获取当前小说的详情信息
        Book_info = NovelModel.objects.get(id=int(book_id))
        #获取小说是否收藏
        if Collection.objects.filter(user_name=request.user.id, novel_name=Book_info.id):
            mig = "ysc"
        else:
            mig = "wsc"
        # 获取小说章节
        Book_text = NovelChaPter.objects.filter(novelchapter_cover=Book_info.id)
        #获取用户登录后当前阅读的小说记录，以便提示用户继续阅读
        if request.user.is_authenticated():
            try:
                novel_num = ReadNovel.objects.get(user_name=request.user.id, novel_name=int(book_id))
            except:
                novel_num = 0
        #小说详情页面的评论功能显示
        user_info = CommentModels.objects.filter(book_id=int(book_id)).order_by("-comment_data")#[:10]

        #倒叙章节排列
        if request.GET.get("sortType") == "1":
            msg = "dx"
            Book_text = Book_text.order_by("-id")
        #正序章节排列
        if request.GET.get("sortType") == "0":
            msg = "zx"
            Book_text = Book_text.order_by("id")
        # 对小说的章节进行分页
        try:
            page = request.GET.get('page', 1)
            p = Paginator(Book_text, 20, request=request)
            Book_text = p.page(page)
        except EmptyPage:
            page = 1
            Book_text = p.page(page)
        except PageNotAnInteger:
            page = 1
            Book_text = p.page(page)
        except:
            page = 1
            Book_text = p.page(page)
        #在每次浏览的时候让前端显示的用户的浏览量+1
        next = NovelModel.objects.get(id=int(book_id))
        next.novel_next += 1
        next.save()
        return render(request, "book.html", locals())

    #小说的收藏功能
    def post(self, request):
        #判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        #获取用户ID和小说的ID
        user_id = request.POST.get("fav_type",0) #获取用户ID
        book_id = request.POST.get("fav_id",0) #获取小说的ID
        #先判断之前是否收藏过如果收藏过就证明用户要取消收藏
        fave = Collection()
        faves = Collection.objects.filter(user_name=user_id, novel_name=book_id)
        if faves:
            faves.delete()
            faves.update()
            # print("取消收藏成功")
            #取消收藏以后小说的收藏数减1
            fave_num = NovelModel.objects.get(id=book_id)
            fave_num.novel_fave -= 1
            fave_num.save()
            return HttpResponse('{"status":"success", "msg":" "}', content_type='application/json')
        else:
            fave.user_name = user_id
            fave.novel_name = book_id
            fave.save()
            # print("收藏成功")
            #收藏成功后小说的收藏数加1
            fave_num = NovelModel.objects.get(id=book_id)
            fave_num.novel_fave += 1
            fave_num.save()
            return HttpResponse('{"status":"success", "msg":" "}', content_type='application/json')
        # return HttpResponse("收藏",locals())



'''小说的内容页面处理视图'''
class TextView(View):
    def get(self, request, text_id):
        novel_text = NovelChaPter.objects.get(id=int(text_id))
        book = NovelModel.objects.get(novel_name=novel_text.novelchapter_cover.novel_name)
        if book.is_long:
            if not request.user.is_authenticated():
                return render(request, "login.html", locals())

        #判断是否之前阅读过如果阅读过就不增加阅读记录
        if request.user.is_authenticated():
            if not ReadNovel.objects.filter(user_name=request.user.id, novel_name=novel_text.novelchapter_cover.id):
                readnovel = ReadNovel(user_name=request.user.id, novel_name=novel_text.novelchapter_cover.id) #实例化小说的models数据模型
                readnovel.chapter_num = novel_text.id #保存小说的章节ID，以便下次阅读
                readnovel.save()
                #阅读量+1
                read =  NovelModel.objects.get(id=novel_text.novelchapter_cover.id)
                read.novel_read += 1
                read.save()
            else:
                #在阅读记录存在的情况下，只更新当前小说的章节ID
                readnovels = ReadNovel.objects.get(user_name=request.user.id, novel_name=novel_text.novelchapter_cover.id)
                readnovels.chapter_num = novel_text.id
                readnovels.save()
        else:
            # 在没有登陆的情况下值增加阅读量+1
            read = NovelModel.objects.get(id=novel_text.novelchapter_cover.id)
            read.novel_read += 1
            read.save()

        # #在每次浏览的时候让前端显示的用户的浏览量+1
        # next = NovelModel.objects.get(id=novel_text.novelchapter_cover.id)
        # next.novel_next += 1
        # next.save()

        return render(request, "text.html", locals())



'''小说的全局搜索功能'''
class SearchView(View):
    def get(self, request):
        try:
            search_key = request.GET.get("keyword", "")
            if search_key:
                #搜索查询小说
                search_novel = NovelModel.objects.filter(Q(novel_name__icontains=search_key)|Q(novel_text__icontains=search_key))
                #如果没有搜索到就返回no
                if search_novel:
                    #对搜索内容进行排序
                    try:
                        page = request.GET.get('page', 1)
                        p = Paginator(search_novel, 4, request=request)
                        search_novel = p.page(page)
                    except EmptyPage:
                        page = 1
                        search_novel = p.page(page)
                    except PageNotAnInteger:
                        page = 1
                        search_novel = p.page(page)
                    except:
                        page = 1
                        search_novel = p.page(page)
                        print(search_novel)
                    return render(request, "search.html", locals())
            msg = "no"
            return render(request, "search.html", locals())
        except:
            #如果出错就证明没有搜索到小说
            msg = "no"
            return render(request, "search.html", locals())



'''小说的评论加载使用AjAx异步加载''' #--------------> 不会前端这个功能还没有完成
class PingView(View):
    def post(self, request):
        print(request.POST)
        search_novel = CommentModels.objects.filter(book_id=int(request.POST.get("bookid")))
        # # 对搜索内容进行排序
        # try:
        #     page = request.GET.get('page', 1)
        #     p = Paginator(search_novel, 4, request=request)
        #     search_novel = p.page(page)
        # except EmptyPage:
        #     page = 1
        #     search_novel = p.page(page)
        # except PageNotAnInteger:
        #     page = 1
        #     search_novel = p.page(page)
        # except:
        #     page = 1
        #     search_novel = p.page(page)
        #     print(search_novel)
        # return render(request, "search.html", locals())

        #把数据转换成json
        # json_data = serializers.serialize("json", CommentModels.objects.filter(book_id=int(request.POST.get("bookid"))).order_by("-comment_data")[int(request.POST.get("page")):]) #把数据转换成json数据
        # print(list1)
        # return HttpResponse(json_data, content_type='application/json')
        return HttpResponse({"data":"data","title":"title"}, content_type="application/jaon")