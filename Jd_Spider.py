import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import csv

count = 0

file_format = input('请输入文件保存格式（txt、json、csv）：')
while file_format!='txt' and file_format!='json' and file_format!='csv':
    file_format = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')
if file_format=='txt' :
    file = open('Jd.txt','w',encoding='utf-8')
elif file_format=='json' :
    file = open('Jd.json','w',encoding='utf-8')
elif file_format=='csv' :
    file = open('Jd.csv','w',encoding='utf-8',newline='')
    writer = csv.writer(file)

browser = webdriver.Chrome()
browser.implicitly_wait(10)
wait = WebDriverWait(browser,10)
start_url = 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC&enc=utf-8&wq=%E7%AC%94%E8%AE%B0%E6%9C%AC&pvid=e8604bd75a024b31a9aff06b803229ea'
browser.get(start_url)
browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

print('Processing')
while True :
    try:
        symbol = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[2]/strong/i')))
        symbol = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[3]/a/em')))
        symbol = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[4]/strong')))
        #symbol = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[5]/span/a')))
    except selenium.common.exceptions.TimeoutException:
        continue
    else:
        prices = browser.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[2]/strong/i')
        names = browser.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[3]/a/em')
        commits = browser.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[4]/strong')
        #shops = browser.find_elements_by_xpath('//div[@class="gl-i-wrap"]/div[5]/span/a')
        
    if file_format=='txt' :
        for i in range(len(prices)):
            count += 1
            print(count)
            file.write('--------------------'+str(count)+'--------------------\n')
            file.write('price：')
            file.write(prices[i].text)
            file.write('\n')
            file.write('name：')
            file.write(names[i].text)
            file.write('\n')
            file.write('commit：')
            file.write(commits[i].text)
            file.write('\n')
            #file.write('shop：')
            #file.write(shops[i].text)
            #file.write('\n')
    elif file_format=='json' :
        for i in range(len(prices)):
            count += 1
            print(count)
            item = {}
            item['price'] = prices[i].text
            item['name'] = names[i].text
            item['commit'] = commits[i].text
            #item['shop'] = shops[i].text
            json.dump(item,file,ensure_ascii = False)
    elif file_format=='csv' :
        for i in range(len(prices)):
            count += 1
            print(count)
            item = {}
            item['price'] = prices[i].text
            item['name'] = names[i].text
            item['commit'] = commits[i].text
            #item['shop'] = shops[i].text
            for key in item:
                writer.writerow([key, item[key]])
    
    try:
        next_page = browser.find_element_by_xpath('//a[@class="pn-next" and @onclick]')
    except selenium.common.exceptions.NoSuchElementException:
        break
    else:
        next_page.click()
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

file,close()
browser.quit()
print('Finished')
