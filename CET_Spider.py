from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import re
import time
import requests
import sys

opt = webdriver.chrome.options.Options()
opt.set_headless()
browser = webdriver.Chrome(chrome_options=opt)
browser.get('http://cet.neea.edu.cn/cet/')
browser.implicitly_wait(10)
wait = WebDriverWait(browser,10)

try:
    num_bar = wait.until(EC.presence_of_element_located((By.ID,'zkzh')))
    num = input('请输入你的准考证号：')
    while re.search(r'^\d{15}$', num)==None :
        num = input('输入错误，请重新输入你的准考证号：')
    num_bar.send_keys(num)

    name_bar = wait.until(EC.presence_of_element_located((By.ID,'name')))
    name = input('请输入你的姓名：')
    while re.search(r'[\u4e00-\u9fa5]', name)==None :
        name = input('输入错误，请重新输入你的姓名：')
    name_bar.send_keys(name)

    ver_bar = wait.until(EC.presence_of_element_located((By.ID,'verify')))
    ver_bar.click()
    time.sleep(1)

    img = wait.until(EC.presence_of_element_located((By.ID,'img_verifys')))
    response = requests.get(img.get_attribute('src'))
    with open('验证码.PNG','wb') as f:
        f.write(response.content)
        
    ver = input('请输入验证码（图片已保存在当前目录下）：')
    ver_bar.send_keys(ver)

    button = wait.until(EC.presence_of_element_located((By.ID,'submitButton')))
    button.click()
    time.sleep(1)
except selenium.common.exceptions.Exception as e:
    print(str(e))
    sys.exit()

try:
    print('---------------查询结果如下---------------')
    name = wait.until(EC.presence_of_element_located((By.ID,'n')))
    print('姓名：'+ name.text)
    school = wait.until(EC.presence_of_element_located((By.ID,'x')))
    print('学校：'+ school.text)
    print('----------笔试成绩----------')
    total = wait.until(EC.presence_of_element_located((By.ID,'s')))
    print('总分：'+ total.text)
    listening = wait.until(EC.presence_of_element_located((By.ID,'l')))
    print('听力：'+ listening.text)
    reading = wait.until(EC.presence_of_element_located((By.ID,'r')))
    print('阅读：'+ reading.text)
    writing = wait.until(EC.presence_of_element_located((By.ID,'w')))
    print('写作和翻译：'+ writing.text)
    print('----------口语成绩----------')
    speaking = wait.until(EC.presence_of_element_located((By.ID,'kys')))
    print('等级：'+ speaking.text)
except selenium.common.exceptions.UnexpectedAlertPresentException as e:
    print(str(e))
    sys.exit()

browser.quit()
