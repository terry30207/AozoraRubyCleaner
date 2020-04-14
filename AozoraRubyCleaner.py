from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import os







url=input("請輸入網址")  # 輸入範例網址，交給瀏覽器 
#url="https://www.aozora.gr.jp/cards/001518/files/51731_50813.html"
#url="https://www.aozora.gr.jp/cards/000281/files/43266_35637.html"
#url="https://www.aozora.gr.jp/cards/000291/files/58235_68277.html"
browser=webdriver.PhantomJS(executable_path=os.path.abspath(os.path.dirname(__file__))+'\\phantomjs.exe')
browser.get(url)
pageSource = browser.page_source  # 取得網頁原始碼
soup = BeautifulSoup(pageSource, 'html.parser')

for rt in soup("rt"):
    rt.decompose()
for rp in soup("rp"):
    rp.decompose()
for sup in soup("sup"):
    sup.decompose()
for div in soup.find_all("div", {'class':'jisage_2'}): 
    div.decompose()
for div in soup.find_all("div", {'id':'contents'}): 
    div.decompose()
for div in soup.find_all("div", {'class':'bibliographical_information'}): 
    div.decompose()
for div in soup.find_all("div", {'class':'notation_notes'}): 
    div.decompose()
for div in soup.find_all("div", {'id':'card'}): 
    div.decompose()
soup_string = str(soup)
aa=r'\<.*?\>'
ext = re.sub(aa, '', soup_string)

a=r'※［.*?、'

ext = re.sub(a, '', ext)

b=r'、.*?］'
ext=re.sub(b,'',ext)

c=r'U\+....'
res=re.search(c,ext)
while res!= None:
    chr=res.group(0)[2]+res.group(0)[3]+res.group(0)[4]+res.group(0)[5]
    chr='\\u'+chr
    chr=chr.encode('latin-1').decode('unicode_escape')
    ext=re.sub(c,chr,ext,1)
    res=re.search(c,ext)
print(ext)
txtfile=open(os.path.abspath(os.path.dirname(__file__))+"\\"+ "ruby_free.txt" ,'w',encoding = 'utf8')
txtfile.write(ext)
txtfile.close()

browser.close()