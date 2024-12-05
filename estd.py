from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import date, timedelta



class Finder:
    
    def __init__(self):
        
        self.chrome_driver_path = "/Python Works/selenium/chromedriver"
        self.browserProfile = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(self.chrome_driver_path, options=self.browserProfile)
        
        self.my_dict = {}
    
    def saveToFile(self, item):
        with open(f'urls.jsonl', encoding="utf-8", mode='a') as file:
            s = json.dumps(item, sort_keys = False, ensure_ascii=False) + '\n'
            file.write(s)
    
    def getLinks(self, page, name, date):
        
        self.browser.get(page)
        action = webdriver.ActionChains(self.browser)
       
        c = self.browser.find_element_by_css_selector('p.flt-registros').text
        b = re.findall(r'\d+',c)[0]
        print(f'There are {b} news!')
        b = int(b)
        times = int(b/10) + 3
        time.sleep(1)
        while True:
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(0.5)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(0.5)
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(0.5)
            
            button = self.browser.find_elements_by_css_selector("div.box.line")[-1].find_element_by_tag_name('a')
            self.browser.execute_script("arguments[0].click();", button)
            liste = self.browser.find_elements_by_class_name('link-title')
            a = len(liste)
            if a == b:
                print(f'All {a} news are uploaded')
                break
            else:
                print(a)
                
        for url in liste:
            self.my_dict['date'] = date
            self.my_dict['html_page'] = f'{name}.html'
            self.my_dict['url'] = url.get_attribute('href')
            self.saveToFile(self.my_dict)
            self.my_dict = {}
            
         
        with open(f'html/{name}.html', 'w') as file:
            file.write(self.browser.page_source)
        print(f"{name}: page source is saved!")
        
def date_generator(start_date, end_date):
    '''
    Day generator between two dates
    '''
    delta = end_date - start_date
    liste = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        s = day.strftime('%d-%m-%Y') + '\n'
        with open('date.txt', 'a') as file:
            file.write(s)
            print(s)
            
date_generator(date(2018, 6, 22), date(2022, 2, 13))

finder = Finder()  

line_1 = "https://busca.estd.com.br/?tipo_conteudo=Not%C3%ADcias&quando="
with open('date.txt') as file:
    lines = file.readlines()

id = 1
for date in lines:
    
    j = date[:-1].split('-')
    d = j[0]
    m = j[1]
    y = j[2]
    name = f'{d}_{m}_{y}'
    datee = f'{d}/{m}/{y}'
    line_2 = f'{d}%2F{m}%2F{y}-{d}%2F{m}%2F{y}&q='
    page = line_1 + line_2
    finder.getLinks(page, name, datee)
    print(f'{id}: {date[:-1]} saved!')
    id +=1
          
print('Process finished!')
