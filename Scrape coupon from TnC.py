#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('window-size=1920x1480')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
CHROMEDRIVER_PATH = 'E:/GOMMT/Solve for Tomorrow (6292020)/Selenium/chromedriver.exe'
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)


# In[2]:


driver.get("https://www.easemytrip.com/")
driver.maximize_window()


# In[3]:


button = driver.find_element_by_xpath('//*[@id="myTopnav"]/div[1]/ul/li[1]/a')
webdriver.ActionChains(driver).move_to_element(button).perform()
time.sleep(2)
webdriver.ActionChains(driver).click(button).perform()


# In[4]:


# From https://www.easemytrip.com/flights.html
List = driver.find_element_by_xpath('/html/body/div[13]/div/div/ul')
allElements = List.find_elements_by_tag_name("a")
links = []
for element in allElements:
    links.append(element.get_attribute("href"))


# In[5]:


driver.get("https://www.easemytrip.com/deals.html")
# driver.maximize_window()
button = driver.find_element_by_xpath('/html/body/div[1]/div/a[2]/span')
webdriver.ActionChains(driver).move_to_element(button).perform()
time.sleep(2)
webdriver.ActionChains(driver).click(button).perform()


# In[6]:


content = driver.page_source
soup = BeautifulSoup(content)
for offer in soup.findAll('div', attrs={'class':'offer-box'}):
    links.append(offer.find('div', attrs={'class':'reveal'}).find()['href'])
links.pop()


# In[7]:


class coupon:
    def __init__(self, code, what_You_Get,How_do_you_get_it,What_else_do_you_need_to_know,Terms_and_Conditions):
        self.code = code
        self.what_You_Get = what_You_Get
        self.How_do_you_get_it = How_do_you_get_it
        self.What_else_do_you_need_to_know = What_else_do_you_need_to_know
        self.Terms_and_Conditions = Terms_and_Conditions


# In[8]:


couponList = []
for link in links:
    driver.get(link)
    content = driver.page_source
    soup = BeautifulSoup(content)
    try:
        code = soup.find('div', attrs={'class':'cp_code'}).text
    except Exception:
        code = 'NULL'
    i = 1
    ele = soup.findAll('ul', attrs={'class':'dot-list'})
    a = ''.join(ele[0].findAll(text=True)).strip()
    b = ''.join(ele[1].findAll(text=True)).strip()
    c = ''.join(ele[2].findAll(text=True)).strip()
    d = ''.join(ele[3].findAll(text=True)).strip()
    x = coupon(code,a,b,c,d)
    couponList.append(x)
driver.close()


# In[9]:


Code = []
what_You_Get = []
How_do_you_get_it = []
What_else_do_you_need_to_know = []
Terms_and_Conditions = []
for coupon in couponList:
    Code.append(coupon.code)
    what_You_Get.append(coupon.what_You_Get)
    How_do_you_get_it.append(coupon.How_do_you_get_it)
    What_else_do_you_need_to_know.append(coupon.What_else_do_you_need_to_know)
    Terms_and_Conditions.append(coupon.Terms_and_Conditions)


# In[10]:


df = pd.DataFrame({'Code': Code,
                   'What you get?': what_You_Get,
                   'How do you get it?': How_do_you_get_it,
                   'What else do you need to know?': What_else_do_you_need_to_know,
                   'Terms and Conditions': Terms_and_Conditions}) 
df.to_csv('CoupounsTnCdata.csv', index=False, encoding='utf-8')

