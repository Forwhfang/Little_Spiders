import urllib.request
import urllib.parse
import json

#把接口封装成一个函数
def translate(content):
    #考虑特殊情况
    if content == "" :
        return ""
    
    #起始URL
    url = "http://fanyi.youdao.com/translate" 
    
    #构造POST请求的Form Data
    params = {
        'i':content,
        'doctype':'json',
        'from':'AUTO'
        'to''AUTO'
    }
    data = urllib.parse.urlencode(params).encode('utf-8')
    
    #构造Request Headers
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    
    #构造Request对象
    req = urllib.request.Request(url,data=data,headers=headers,method='POST')
    
    #发送请求，得到响应
    response = urllib.request.urlopen(req)
    
    #解析数据
    result = json.loads(response.read().decode('utf-8'))
    return result['translateResult'][0][0]['tgt']

if __name__ == "__main__":
    print('请输入翻译内容，输入"quit"退出')
    while(True):
        content = input('翻译内容：')
        if(content == 'quit'):
            break
        result = translate(content)
        print("翻译结果：%s" % result)
