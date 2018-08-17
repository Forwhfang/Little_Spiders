#-*-coding:utf-8-*-
import urllib.request
import urllib.parse
import re
import time
import random

class TiebaSpider():
    #初始化
    def init(self):
        #用户输入的搜索关键字，即主题贴吧名称
        self.keyword = input('请输入主题贴吧名字：')
        #网页的初始化链接地址，用urllib.parse.quote()函数可以对中文进行转码
        self.base_url = 'http://tieba.baidu.com/f?kw=' + urllib.parse.quote(self.keyword) + '&ie=utf-8&pn={page}'

    #获得网页源代码
    def get_page(self,page):
        #请求信息：Request URL
        url = self.base_url.format(page=page)
        #请求信息：Request Headers
        headers = {
            'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        #构造请求对象
        req = urllib.request.Request(url=url,headers=headers,method='GET')
        #发送请求，得到响应
        response = urllib.request.urlopen(req)
        #获得网页源代码
        html = response.read().decode('utf-8')
        #返回网页源代码
        return html

    #解析网页源代码，提取数据
    def parse_page(self,html):
        #帖子的主题名称
        titles = re.findall(r'href="/p/\d+" title="(.+?)"',html)
        #帖子的主题作者
        authods = re.findall(r'title="主题作者: (.+?)"',html)      
        #帖子的链接地址
        nums = re.findall(r'href="/p/(\d+)"',html)
        links = []
        for item in nums:
            links.append('http://tieba.baidu.com/p/' + item)
        #帖子的回复数量
        focus = re.findall(r'title="回复">(\d+)',html)    
        #帖子的创建时间
        ctimes = re.findall(r'title="创建时间">(.+?)<',html)
        #将所有的信息储存在列表中，列表的每一项为一个字典，对应一个主题帖子的信息
        result = []
        for i in range(len(titles)):
            item = {}
            item['title'] = titles[i]
            item['authod'] = authods[i]
            item['link'] = links[i]
            item['focus'] = focus[i]
            item['ctime'] = ctimes[i]
            result.append(item)
        #返回列表
        return result


    def start_spider(self):
        #初始化
        self.init()
        #获取总共的帖子数量，便于构造URL
        html = self.get_page(0)
        total_page = re.findall(r'共有主题数<span class="red_text">(\d+)</span>个',html)
        total_page = int(total_page[0])
    	#构造URL获取每一页的帖子信息
        page = 0
        count = 0
        f = open(spider.keyword+'.txt','w',encoding='utf-8')
        print('Processing...')
        while  page <= total_page :
            html = self.get_page(page)
            result = self.parse_page(html)
            for i in range(len(result)):
                count += 1
                f.write('--------------------'+str(count)+'--------------------\n')
                f.write(result[i]['title'])
                f.write('\n')
                f.write(result[i]['authod'])
                f.write('\n')
                f.write(result[i]['link'])
                f.write('\n')
                f.write(result[i]['focus'])
                f.write('\n')
                f.write(result[i]['ctime'])
                f.write('\n')
                print(count)
            page += 50
            time.sleep(random.random())
        f.close()
        print('Finished')
    
    
if __name__ == '__main__':
    spider = TiebaSpider()
    spider.start_spider()
