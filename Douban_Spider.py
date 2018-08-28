import requests
from lxml import etree
import time
import random
import json
import csv

class DoubanSpider():
    #初始化
    def init(self):
        #请求的首页
        self.base_url = 'https://movie.douban.com/top250?start={page}&filter='
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
        #发送请求，得到响应
        response = requests.get(url=url,headers=headers)
        #返回响应体
        return response.text

    #解析网页源代码
    def parse_html(self,html):
        #构造_Element对象
        html = etree.HTML(html)
        #电影的详细链接
        links = html.xpath('//div[@class="hd"]/a/@href')
        #电影的名字
        titles = html.xpath('//div[@class="hd"]/a/span[1]/text()')
        #电影的信息（导演/主演、上映年份/国家/分类）
        info = html.xpath('//div[@class="bd"]/p[1]//text()')
        #电影的评分
        stars = html.xpath('//div[@class="bd"]/div/span[2]/text()')
        #电影的评论人数
        comments = html.xpath('//div[@class="bd"]/div/span[4]/text()')
        #将所有的信息储存在列表中，列表的每一项为一个字典，对应一部电影的信息
        result = []
        for i in range(25):
            data = {}
            data['link'] = links[i].encode('utf-8').decode('utf-8')
            data['title'] = titles[i].encode('utf-8').decode('utf-8')
            data['role'] = info[2*i].encode('utf-8').decode('utf-8').strip()
            data['descrition'] = info[2*i+1].encode('utf-8').decode('utf-8').strip()
            data['star'] = stars[i].encode('utf-8').decode('utf-8')
            data['comment'] = comments[i].encode('utf-8').decode('utf-8')
            result.append(data)
        #返回列表
        return result

    #开始爬取                   
    def crawl(self):
        #初始化
        self.init()
        #数据初始化
        page = 0
        count = 0
        print('Processing')
        #文件保存格式为.txt
        if self.format=='txt' :
            file = open('douban.txt','w',encoding='utf-8')
            while  page < 250 :
                url = self.base_url.format(page=page)
                html = self.get_html(url)
                result = self.parse_html(html)
                for item in result:
                    count += 1
                    print(count)
                    file.write('--------------------'+str(count)+'--------------------\n')
                    file.write('link：')
                    file.write(item['link'])
                    file.write('\n')
                    file.write('title：')
                    file.write(item['title'])
                    file.write('\n')
                    file.write('role：')
                    file.write(item['role'])
                    file.write('\n')
                    file.write('descrition：')
                    file.write(item['descrition'])
                    file.write('\n')
                    file.write('star：')
                    file.write(item['star'])
                    file.write('\n')
                    file.write('comment：')
                    file.write(item['comment'])
                    file.write('\n')
                page += 25
                time.sleep(random.random())
            file.close()
        #文件保存格式为.json
        if self.format=='json' :
            file = open('douban.json','w',encoding='utf-8')
            while  page < 250 :
                url = self.base_url.format(page=page)
                html = self.get_html(url)
                result = self.parse_html(html)
                for item in result:
                    count += 1
                    print(count)
                    json.dump(item,file,ensure_ascii = False)
                page += 25
                time.sleep(random.random())
            file.close()
        #文件保存格式为.csv
        if self.format=='csv' :
            file = open('douban.csv','w',encoding='utf-8',newline='')
            writer = csv.writer(file)
            while  page < 250 :
                url = self.base_url.format(page=page)
                html = self.get_html(url)
                result = self.parse_html(html)
                for item in result:
                    count += 1
                    print(count)
                    for key in item:
                        writer.writerow([key, item[key]])
                page += 25
                time.sleep(random.random())
            file.close()
        print('Finished')
        
            
if __name__ == "__main__":
    spider = DoubanSpider()
    spider.crawl()
