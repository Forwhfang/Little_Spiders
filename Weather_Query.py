import requests

def weather(cityName):
    #起始URL
    url = 'https://www.sojson.com/open/api/weather/json.shtml?city=' + str(cityName)
    #发送请求，得到响应
    response = requests.get(url)
    #处理返回的数据
    result = response.json()
    if result['message']=='Success !' :
        return result['data']
    else:
        return None
        
        
if __name__ == '__main__':
    print('请输入城市名称，输入"quit"退出：')
    while True :
        #用户输入待查询的城市名称
        cityName = input('城市名称：')
        #考虑特殊情况
        if cityName=='quit' :
            print('程序已退出，欢迎再次使用')
            break
        #考虑特殊情况
        result = weather(cityName)
        if result==None :
            print('查询结果错误，请检查城市名称并再次输入')
            continue
        #若一切正常，则打印出查询结果
        print('---------------Processing---------------')
        print('------------------------------')
        print('温度：',result['wendu'])
        print('湿度：',result['shidu'])
        print('PM10：',result['pm10'])
        print('PM2.5：',result['pm25'])
        print('空气质量：',result['quality'])
        print('感冒提醒：',result['ganmao'])
        print('------------------------------')
        for item in result['forecast']:
            print('日期：',item['date'])
            print('风力：',item['fl'])
            print('风向：',item['fx'])
            print('最高温：',item['high'])
            print('最低温：',item['low'])
            print('温馨提醒：',item['notice'])
            print('日出时间：',item['sunrise'])
            print('日落时间：',item['sunset'])
            print('天气：',item['type'])
            print('------------------------------')
        print('---------------Finished---------------')
