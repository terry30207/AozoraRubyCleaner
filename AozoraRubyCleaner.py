from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re
import os







url=input("請輸入網址\n")  # get page url 
browser=webdriver.PhantomJS(executable_path=os.path.abspath(os.path.dirname(__file__))+'\\phantomjs.exe')       # "Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead" 
                                                                                                                #NOT NOW.
browser.get(url)
pageSource = browser.page_source  # get html of the url
soup = BeautifulSoup(pageSource, 'html.parser')# create BS object

for rt in soup("rt"):    #remove all the <rt> tags, which means all the kana char above kanji
    rt.decompose()
for rp in soup("rp"):    #remove all the <rp> tags, which means char to show while rt tag isn't support by browser
    rp.decompose()
for sup in soup("sup"):    #remove all the <sup> tags, which means all footnotes
    sup.decompose()
for div in soup.find_all("div", {'class':'jisage_2'}):    #remove all the explanation
    div.decompose()
for div in soup.find_all("div", {'id':'contents'}):     #remove contents
    div.decompose()
for div in soup.find_all("div", {'class':'bibliographical_information'}):   #remove info of the original book and info of the file maker
    div.decompose()
for div in soup.find_all("div", {'class':'notation_notes'}):    #remove "about notation"
    div.decompose()
for div in soup.find_all("div", {'id':'card'}):     #remove card link
    div.decompose()
soup_string = str(soup)
aa=r'\<.*?\>'
ext = re.sub(aa, '', soup_string)   #remove other tags

#For those chars not in JIS, they notate like this: ※［＃「匈／（胃－田）」、U+80F7、32-本文-3］
#Thus, codes below turns above notation back to correct char

a=r'※［.*?、'
ext = re.sub(a, '', ext)#remove all the chars between '※' and the first '、'

b=r'、.*?］'
ext=re.sub(b,'',ext)#remove all the chars between second '、' and '］'

c=r'U\+....'    
res=re.search(c,ext)    #get the first unicode match the pattern 'U+XXXX'
while res!= None:   #while found:
    chr=res.group(0)[2]+res.group(0)[3]+res.group(0)[4]+res.group(0)[5]     #remove 'U+', str.strip just won't work and only god knows why
    chr='\\u'+chr   #make pattern '\uXXXX'
    chr=chr.encode('latin-1').decode('unicode_escape')      #convert to correct char
    ext=re.sub(c,chr,ext,1)     #remove the pattern 'U+XXXX' and put the correct char back
    res=re.search(c,ext)        #try to find next unicode
print(ext)    #show in command line
txtfile=open(os.path.abspath(os.path.dirname(__file__))+"\\"+ "ruby_free.txt" ,'w',encoding = 'utf8')
txtfile.write(ext)
txtfile.close()    #write to the txt file
print("完成")
browser.close() #close phantomJS