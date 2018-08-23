import requests
from lxml import etree
import time
import random

class DoubanSpider():
    movieID = ""
    
    def init(self):
        self.movieID = input('请输入电影ID：')
    
    def get_html(self,url):
        headers = {
            'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url=url,headers=headers)
        return response.text

    def parse_page(self,html):
        html = etree.HTML(html)
        agrees = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[1]/span/text()')
        authods = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/a/text()')
        stars = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/span[2]/@title')
        contents = html.xpath('//div[@class="comment-item"]/div[2]/p/span/text()')
        result = []
        for i in range(len(agrees)):
            data = {}
            data['agree'] = agrees[i].encode('utf-8').decode('utf-8')
            data['authod'] = authods[i].encode('utf-8').decode('utf-8')
            data['star'] = stars[i].encode('utf-8').decode('utf-8')
            data['content'] = contents[i].encode('utf-8').decode('utf-8')
            result.append(data)
        return result

    def parse_link(self,html):
        html = etree.HTML(html)
        base_url = 'https://movie.douban.com/subject/'+str(self.movieID)+'/comments'
        url = html.xpath('//div[@id="paginator"]/a[@class="next"]/@href')
        if not url :
            return "END"
        link = base_url + url[0].encode('utf-8').decode('utf-8')
        return link

    def crawl(self):
        print('Processing')
        file = open('douban.txt','w',encoding='utf-8')
        url = 'https://movie.douban.com/subject/' + str(self.movieID) + '/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
        count = 0
        while True :
            time.sleep(random.random())
            html = self.get_html(url)
            result = self.parse_page(html)
            for item in result:
                count += 1
                print(count)
                file.write('--------------------'+str(count)+'--------------------\n')
                file.write('评论者：')
                file.write(item['authod'])
                file.write('\n')
                file.write('赞同人数：')
                file.write(item['agree'])
                file.write('\n')
                file.write('评价：')
                file.write(item['star'])
                file.write('\n')
                file.write('评论内容：')
                file.write(item['content'])
                file.write('\n')
            url = self.parse_link(html)
            if url=='END' :
                break
        file.close()
        print('Finished')

if __name__ == "__main__":
    spider = DoubanSpider()
    spider.init()
    spider.crawl()
