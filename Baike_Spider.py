from lxml import etree
import urllib.request
import urllib.parse

def crawl(content):
    if content == "":
        return ""
    url = 'https://baike.baidu.com/item/' + urllib.parse.quote(content)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers, method='GET')
    response = urllib.request.urlopen(req)
    text = response.read().decode('utf-8')
    html = etree.HTML(text)
    sen_list_with_n = html.xpath('//div[contains(@class,"lemma-summary") or contains(@class,"lemmaWgt-lemmaSummary")]//text()')
    sen_list = [elem for elem in sen_list_with_n if not '\n' in elem]
    return ''.join(sen)

if __name__ == '__main__':
    while (True):
        content = input('查询词语：')
        result = crawl(content)
        print("查询结果：%s" % result)
