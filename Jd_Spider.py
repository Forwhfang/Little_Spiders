from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import json
import csv
import time


class JdSpider():
    def init(self):        
        self.file_format = input('请输入文件保存格式（txt、json、csv）：')
        while self.file_format!='txt' and self.file_format!='json' and self.file_format!='csv':
            self.file_format = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')
        if self.file_format=='txt' :
            self.file = open('Jd.txt','w',encoding='utf-8')
        elif self.file_format=='json' :
            self.file = open('Jd.json','w',encoding='utf-8')
        elif self.file_format=='csv' :
            self.file = open('Jd.csv','w',encoding='utf-8',newline='')#
            self.writer = csv.writer(self.file)
        print('File Initialized')

        self.prices = []
        self.names = []
        self.commits = []
        self.count = 0
        self.start_url = 'https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC&enc=utf-8&pvid=c4fa7a2ce8f64c8dbe121a5edac4add2'
        print('Data Initialized')

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)
        self.wait = WebDriverWait(self.browser,10)
        print('Browser Initialized')
    
    def parse_page(self):
        try:
            self.prices = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[2]/strong/i')))
            self.names = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[3]/a/em')))
            self.commits = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="gl-i-wrap"]/div[4]/strong')))
        except selenium.common.exceptions.TimeoutException:
            print('parse_page:TimeoutException')
            self.parse_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('parse_page:StaleElementReferenceException')
            self.browser.refresh()
        else:
            if len(self.prices)!=60 or len(self.names)!=60 or len(self.commits)!=60:
                print('Trying...')
                self.parse_page()

    def write_to_file(self):
        try:
            if self.file_format=='txt' :
                for i in range(60):
                    self.count += 1
                    print('录入数据：'+str(self.count))
                    self.file.write('--------------------'+str(self.count)+'--------------------\n')
                    self.file.write('price：')
                    self.file.write(self.prices[i].text)
                    self.file.write('\n')
                    self.file.write('name：')
                    self.file.write(self.names[i].text)
                    self.file.write('\n')
                    self.file.write('commit：')
                    self.file.write(self.commits[i].text)
                    self.file.write('\n')
            elif self.file_format=='json' :
                for i in range(60):
                    self.count += 1
                    print('录入数据：'+str(self.count))
                    item = {}
                    item['price'] = self.prices[i].text
                    item['name'] = self.names[i].text
                    item['commit'] = self.commits[i].text                
                    json.dump(item,self.file,ensure_ascii = False)                
            elif self.file_format=='csv' :
                for i in range(60):
                    self.count += 1
                    print('录入数据：'+str(self.count))
                    item = {}
                    item['price'] = self.prices[i].text
                    item['name'] = self.names[i].text
                    item['commit'] = self.commits[i].text
                    for key in item:
                        self.writer.writerow([key, item[key]])
        except selenium.common.exceptions.StaleElementReferenceException:
            print('write_to_file:StaleElementReferenceException')
            self.browser.refresh()

    def turn_page(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH,'//a[@class="pn-next" and @onclick]'))).click()#
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
        except selenium.common.exceptions.NoSuchElementException:
            return True
        except selenium.common.exceptions.TimeoutException:
            print('turn_page:TimeoutException')
            self.page_turning()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('turn_page:StaleElementReferenceException')
            self.browser.refresh()
        else:
            return False

    def close(self):
        self.browser.quit()
        print('Finished')
    
    def crawl(self):
        self.init()
        self.browser.get(self.start_url)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        while True:
            self.parse_page()
            self.write_to_file()
            if self.turn_page()==True :
                break
        self.close()
        
if __name__ == '__main__':
    spider = JdSpider()
    spider.crawl()
