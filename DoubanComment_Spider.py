import requests
from lxml import etree
import time
import random
import json
import csv

class DoubanSpider():
    #初始化
    def init(self):
        #用户输入的电影ID
        self.movieID = input('请输入电影ID：')
        #用户输入的文件保存格式
        self.format = input('请输入文件保存格式（txt、json、csv）：')
        while self.format!='txt' and self.format!='json' and self.format!='csv':
            self.format = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')

    #获取网页源代码
    def get_html(self,url):
        #构造请求头部
        headers = {
            'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        #发送请求，获得响应
        response = requests.get(url=url,headers=headers)
        #返回网页源代码
        return response.text

    #解析网页源代码，获取数据
    def parse_page(self,html):
        #构造_Element对象
        html = etree.HTML(html)
        #赞同人数
        agrees = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[1]/span/text()')
        #评论作者
        authods = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/a/text()')
        #评价
        stars = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/span[2]/@title')
        #评论内容
        contents = html.xpath('//div[@class="comment-item"]/div[2]/p/span/text()')
        #将所有的信息储存在列表中，列表的每一项为一个字典，对应一条评论的信息
        result = []
        for i in range(len(agrees)):
            data = {}
            data['agree'] = agrees[i].encode('utf-8').decode('utf-8')
            data['authod'] = authods[i].encode('utf-8').decode('utf-8')
            data['star'] = stars[i].encode('utf-8').decode('utf-8')
            data['content'] = contents[i].encode('utf-8').decode('utf-8')
            result.append(data)
        #返回列表
        return result

    #解析网页源代码，获取下一页链接
    def parse_link(self,html):
        #构造_Element对象
        html = etree.HTML(html)
        #下一页链接
        base_url = 'https://movie.douban.com/subject/'+str(self.movieID)+'/comments'
        url = html.xpath('//div[@id="paginator"]/a[@class="next"]/@href')
        if not url : #如果匹配为空，则证明是最后一页，返回字符串"END"作为结束标志
            return "END"
        link = base_url + url[0].encode('utf-8').decode('utf-8')
        return link

    #开始爬取
    def crawl(self):
        #初始化
        self.init()
        #数据初始化
        count = 0
        url = 'https://movie.douban.com/subject/' + str(self.movieID) + '/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
        print('Processing')
        #文件保存格式为.txt
        if self.format=='txt' :
            file = open('douban_comment.txt','w',encoding='utf-8')
            while True :
                html = self.get_html(url)
                result = self.parse_page(html)
                for item in result:
                    count += 1
                    print(count)
                    file.write('--------------------'+str(count)+'--------------------\n')
                    file.write('authod：')
                    file.write(item['authod'])
                    file.write('\n')
                    file.write('agree：')
                    file.write(item['agree'])
                    file.write('\n')
                    file.write('star：')
                    file.write(item['star'])
                    file.write('\n')
                    file.write('content：')
                    file.write(item['content'])
                    file.write('\n')
                url = self.parse_link(html)
                if url=='END' :
                    break
                time.sleep(random.random())
            file.close()
        #文件保存格式为.json
        if self.format=='json' :
            file = open('douban_comment.json','w',encoding='utf-8')
            while True :
                html = self.get_html(url)
                result = self.parse_page(html)
                for item in result:
                    count += 1
                    print(count)
                    json.dump(item,file,ensure_ascii = False)
                url = self.parse_link(html)
                if url=='END' :
                    break
                time.sleep(random.random())
            file.close()
        #文件保存格式为.csv
        if self.format=='csv' :
            file = open('douban_comment.csv','w',encoding='utf-8',newline='')
            writer = csv.writer(file)
            while True :
                html = self.get_html(url)
                result = self.parse_page(html)
                for item in result:
                    count += 1
                    print(count)
                    for key in item:
                        writer.writerow([key, item[key]])
                url = self.parse_link(html)
                if url=='END' :
                    break
                time.sleep(random.random())
            file.close()
        print('Finished')

if __name__ == "__main__":
    spider = DoubanSpider()
    spider.crawl()
