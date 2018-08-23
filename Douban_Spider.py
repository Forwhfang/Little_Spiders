import requests
from lxml import etree
import json
import time
import random

class DoubanSpider():
    base_url = 'https://movie.douban.com/top250?start={page}&filter='
    
    def get_html(self,url):
        headers = {
            'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url=url,headers=headers)
        return response.text

    def parse_html(self,html):
        html = etree.HTML(html)
        links = html.xpath('//div[@class="hd"]/a/@href')
        titles = html.xpath('//div[@class="hd"]/a/span[1]/text()')
        info = html.xpath('//div[@class="bd"]/p[1]//text()')
        stars = html.xpath('//div[@class="bd"]/div/span[2]/text()')
        comments = html.xpath('//div[@class="bd"]/div/span[4]/text()')
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
        return result
                   
    def crawl(self):
        print('Processing')
        file = open('douban.txt','w',encoding='utf-8')
        count = 0
        for i in range(0,250,25):
            time.sleep(random.random())
            url = self.base_url.format(page=i)
            html = self.get_html(url)
            result = self.parse_html(html)
            for item in result:
                count += 1
                print(count)
                file.write('--------------------'+str(count)+'--------------------\n')
                file.write('详细链接：')
                file.write(item['link'])
                file.write('\n')
                file.write('电影名称：')
                file.write(item['title'])
                file.write('\n')
                file.write('导演/主演：')
                file.write(item['role'])
                file.write('\n')
                file.write('上映年份/国家/分类：')
                file.write(item['descrition'])
                file.write('\n')
                file.write('豆瓣评分：')
                file.write(item['star'])
                file.write('\n')
                file.write('评论人数：')
                file.write(item['comment'])
                file.write('\n')
        file.close()
        print('Finished')
        
            
if __name__ == "__main__":
    spider = DoubanSpider()
    spider.crawl()
