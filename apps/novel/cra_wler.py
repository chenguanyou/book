import requests#用于爬虫功能
import re #这里用于验证正则
from bs4 import BeautifulSoup, BeautifulStoneSoup #用于爬虫功能


class Novel_list(object):

    def __init__(self, xiangqing_url, UserAgent ):
        self.xiangqing_url = xiangqing_url
        self.requs = requests.session()
        self.headers = {
            "User-Agent": UserAgent,
        }


    '''获取小说的所有小说解析后html文件的方法'''
    def get_url(self):
        self.url_get = self.requs.get(self.xiangqing_url, headers=self.headers)
        self.url_jie = BeautifulSoup(self.url_get.text, "html5lib")
        return self.url_jie


    '''获取小说列表的url，用于小说详情页面的采集'''
    def get_novel_url(self, url_path):
        self.url_list = []
        self.urls = self.url_jie.select(url_path)
        for self.urls1 in self.urls:
            self.url_xi_num1 = self.urls1.get("href")[23:-1]
            self.url_xi_num2 = re.findall(r'\d+', str(self.urls1))
            for self.url_num in self.url_xi_num2:
                if self.url_num == self.url_xi_num1:
                    self.url_list_data = {
                        'title': self.urls1.get_text(),
                        'url': self.urls1.get("href")
                    }
                    self.url_list.append(self.url_list_data)
        return self.url_list


    '''获取小说url链接里面详情内容'''
    def get_novel_datalis(self, title, image, cat, type, sun, url):
        self.novel_list = []
        for self.url_list1 in self.url_list:
            self.novel_datalis_get = self.requs.get(self.url_list1['url'])
            self.novel_datalis_jie = BeautifulSoup(self.novel_datalis_get.text, "html5lib")
            #获取详情内容
            self.novel_datalis_title = self.novel_datalis_jie.select(title)
            self.novel_datalis_image = self.novel_datalis_jie.select(image)
            self.novel_datalis_cat = self.novel_datalis_jie.select(cat)
            self.novel_datalis_type = self.novel_datalis_jie.select(type)
            self.novel_datalis_sun = self.novel_datalis_jie.select(sun)
            self.novel_datalis_url = self.novel_datalis_jie.select(url)
            for self.novel_title, self.novel_image, self.novel_cat, self.novel_type, self.novel_sun, self.novel_url in zip(self.novel_datalis_title, self.novel_datalis_image, self.novel_datalis_cat, self.novel_datalis_type, self.novel_datalis_sun, self.novel_datalis_url):
                self.novel_data = {
                    'title': self.novel_title.get_text()[:20].strip(),
                    'image': self.novel_image.get("src"),
                    'cat': self.novel_cat.get_text(),
                    'type': self.novel_type.get_text()[39:-10].strip(),
                    'sum': self.novel_sun.get_text().strip(),
                    'url': self.novel_url.get("href")
                }
                self.novel_list.append(self.novel_data)
        return self.novel_list

    '''获取小说的章节列表url'''
    def get_chapter_list(self, chapterurl):
        self.chapter_list_data = []
        for self.chapter_url in self.novel_list:
            # print(self.chapter_url['title'])
            self.chapter_get = self.requs.get(self.chapter_url['url'])
            self.chapter_jie = BeautifulSoup(self.chapter_get.text, "html5lib")
            self.chapter_title = self.chapter_jie.select(chapterurl)
            for self.chapter_list in self.chapter_title:
                self.data = {
                    'title': self.chapter_list.get_text().strip(),
                    'url': self.chapter_list.get("href")
                }
                self.chapter_list_data.append(self.data)
                # print(self.data)

    def get_novel_text(self, title, citys):
        for self.novel_text_url in self.chapter_list_data:
            # print(self.novel_text_url['title'])
            self.novel_text_get = self.requs.get(self.novel_text_url['url'])
            self.novel_text_jie = BeautifulSoup(self.novel_text_get.text, "html5lib")
            self.novel_text_title = self.novel_text_jie.select(title)
            self.novel_text_text = str(self.novel_text_jie.select(citys)).rfind("<p>	<cite>")
            self.novel_text_text1 = str(self.novel_text_jie.select(citys))[:self.novel_text_text]
            for self.novel_title in self.novel_text_title:
                self.novel_text_data = {
                    'title': self.novel_title.get_text(),
                    'city': self.novel_text_text1,
                }
                # print(self.novel_text_data)


'''实例化一个小说源码解析'''
zhangjie = Novel_list("http://www.zhulang.com/Shuku/index/full/1/main/02/sub/all/size/0/flag/2/time/0/type/0/order/0/ini/0/p/2.html",
                      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")

'''使用get_url方法进行解析'''
a2 = zhangjie.get_url()
url = zhangjie.get_novel_url("body > div.main > div > table > tbody > tr > td > a ")\

a = zhangjie.get_novel_datalis("body > div.main.cover-content > div.cover-mian-row > div.cover-left > div.bdrbox.cover-box.clearfix > div.cover-box-right > div.cover-tit > h2",
                           "body > div.main.cover-content > div.cover-mian-row > div.cover-left > div.bdrbox.cover-box.clearfix > div.cover-box-left > img",
                           "body > div.main.cover-content > div.cover-mian-row > div.cover-left > div.bdrbox.cover-box.clearfix > div.cover-box-right > div.cover-tit > p > span",
                           "body > div.main.cover-content > div.cover-mian-row > div.cover-left > div.bdrbox.cover-box.clearfix > div.cover-box-right > div.cover-tit > p ",
                           "#book-summary > p.summ-part",
                           "#chapter-con > div > div.chapter-btn > a.btn.btn-primary")

zhangjie.get_chapter_list("body > div.main.cover-content > div.cover-mian-row > div > div > div.catalog-cnt > div.chapter-list > ul > li > a")

a1 = zhangjie.get_novel_text("#read-content > h2", "#read-content > p")

print(a)

# print(a)
