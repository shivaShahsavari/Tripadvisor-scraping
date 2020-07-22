import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import selenium
from selenium import webdriver
import time
import re

os.chdir('D:\\modules\\Exsell\\Exsell_Programming') # Your working directory
df = pd.read_csv('citylinks.csv') # The file I shared you


def res_info(res_url, name):
    column_names=['Name','TripAdvisorLink','status','pricestatus','adress','city','phone','email','website','rating','reviews','subcat','detail','Thuisbezorgd','TheFork']
    res_info=pd.DataFrame(columns=column_names)
    user_agent_old_phone = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    res_header={'User-Agent': user_agent_old_phone}
    results_res = ''
    while results_res == '':
        try:
            results_res = requests.get(res_url, headers=res_header)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    #results_res = requests.get(res_url, headers=res_header)
    soup_res = BeautifulSoup(results_res.text, "html.parser")
    link=res_url
    Name=status=priceStatus=address=phone=overallRating=reviews=delivery=reserve=''
    try:
        Name=soup_res.find('h1',class_="_3a1XQ88S").text
        status=soup_res.find('div',class_="_1NXh105y").text
        priceStatus=soup_res.find('a',class_="_2mn01bsa").text
        address=soup_res.find('a',href="#MAPVIEW").text
        a=soup_res.find_all('span',class_="_13OzAOXO _2VxaSjVD")
        b=re.findall('<a class="_3S6pHEQs".+?</a>', str(a))
        c=re.sub(r'<a class="_3S6pHEQs" href=.+?">', '', str(b), flags=re.MULTILINE)
        phone=re.sub(r'</a>', '', str(c), flags=re.MULTILINE)
        overallRating=soup_res.find('span',class_="r2Cf69qf").text
        reviews=soup_res.find('a',class_="_10Iv7dOs").text
        aa=soup_res.find_all('img',class_="_3KMxQ_rq")
        delivery=re.findall('thuisbezorgd',str(aa))
        reserve=re.findall('TheFork',str(aa))
    except:
        pass
    subcat=detail=detail1=''
    subtext=soup_res.find_all('div',class_="jT_QMHn2")
    at=soup_res.find_all('div',class_="o3o2Iihq")
    bt=soup_res.find_all('div',class_="_2170bBgV")
    at1=soup_res.find_all('div',class_="_14zKtJkz")
    bt1=soup_res.find_all('div',class_="_1XLfiSsv")
    for i in range(len(subtext)):
        a=re.findall('<span class="_2vS3p6SS">.+?</span>',str(subtext[i]))
        a_sub=re.sub(r'</span>','',re.sub(r'<span class="_2vS3p6SS">', '', str(a), flags=re.MULTILINE),flags=re.MULTILINE)
        b=re.findall('<span class="ui_bubble_rating bubble_.+?"></span>',str(subtext[i]))
        b_sub=re.sub(r'"></span>','',re.sub(r'<span class="ui_bubble_rating bubble_', '', str(b), flags=re.MULTILINE),flags=re.MULTILINE)
        subcat=subcat+a_sub+':'+b_sub+','
    for k in range(len(at)):
        a=re.findall('<div class="o3o2Iihq">.+?</div>',str(at[k]))
        a_sub=re.sub(r'</div>','',re.sub(r'<div class="o3o2Iihq">', '', str(a), flags=re.MULTILINE),flags=re.MULTILINE)
        b=re.findall('<div class="_2170bBgV">.+?</div>',str(bt[k]))
        b_sub=re.sub(r'</div>','',re.sub(r'<div class="_2170bBgV">', '', str(b), flags=re.MULTILINE),flags=re.MULTILINE)
        detail=detail+a_sub+':'+b_sub+','
    for m in range(len(at1)):
        a=re.findall('<div class="_14zKtJkz">.+?</div>',str(at1[m]))
        a_sub=re.sub(r'</div>','',re.sub(r'<div class="_14zKtJkz">', '', str(a), flags=re.MULTILINE),flags=re.MULTILINE)
        b=re.findall('<div class="_1XLfiSsv">.+?</div>',str(bt1[m]))
        b_sub=re.sub(r'</div>','',re.sub(r'<div class="_1XLfiSsv">', '', str(b), flags=re.MULTILINE),flags=re.MULTILINE)
        detail1=detail1+a_sub+':'+b_sub+','
    res_info = res_info.append({'Name': Name if Name else 'N','TripAdvisorLink':link, 'status': status if status else 'N',
    'adress': address if address else 'N','city':str(name),'phone':phone if phone else 'N','email':' ','website':' ',
    'pricestatus':priceStatus if priceStatus else 'N','rating':overallRating if overallRating else 'N',
    'reviews':reviews if reviews else 'N', 'subcat':subcat if subcat else 'N','detail':detail if detail else detail1,
    'Thuisbezorgd':'True' if delivery else 'False','TheFork':'True' if reserve else 'False'}, ignore_index=True)
    time.sleep(5)
    print("details done")
    return res_info


def res_website(res_url):
    column_names=['Name','TripAdvisorLink','website','email']
    user_agent_old_phone = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    res_header={'User-Agent': user_agent_old_phone}
    res_web=pd.DataFrame(columns=column_names)
    results_res = ''
    while results_res == '':
        try:
            results_res = requests.get(res_url, headers=res_header)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    #results_res = requests.get(res_url, headers=res_header)
    soup_res = BeautifulSoup(results_res.text, "html.parser")
    link=res_url
    website1=email=Name=''
    try:
        Name=soup_res.find('h1',class_="_3a1XQ88S").text
        driver.get(res_url)
        time.sleep(2)
        website1=driver.find_element_by_xpath('//a[@target="_blank" and @class="_2wKz--mA _15QfMZ2L"]').get_attribute("href")
        a=soup_res.find_all('div',class_="_36TL14Jn _3jdfbxG0")
        b=re.findall('<a href="mailto:.+?>', str(a))
        c=re.sub(r'<a href="mailto:', '', str(b), flags=re.MULTILINE)
        email=re.sub(r'subject=.+?">', '', str(c), flags=re.MULTILINE)
    except:
        pass
    res_web = res_web.append({'Name': Name if Name else 'N','TripAdvisorLink':link,'website':website1 if website1 else 'N',
    'email':email if email else 'N'}, ignore_index=True)
    #driver.close()
    time.sleep(5)
    print("website done")
    return res_web


df1 = pd.DataFrame()
df2 = pd.DataFrame()
counter = 0
links = df.iloc[9:10,1].to_list() # change the numbers to 10:12
name = df.iloc[9:10,0].to_list() # change the numbers to 10:12
pages = df.iloc[9:10,2].to_list() # change the numbers to 10:12
driver = webdriver.Chrome('C:\\chromedriver_win32\\chromedriver.exe')
for i in range(len(links)):
    for j in range(pages[i]):
        url = 'https://www.tripadvisor.com/Restaurants' +links[i][39:48] +'oa' + str(30 * j) + links[i][47:] + '#EATERY_LIST_CONTENTS'
        results = requests.get(url)
        soup = BeautifulSoup(results.text, "html.parser")
        for sec in soup.find_all('div', class_="_1llCuDZj"):
            a_link = re.findall('<a class="_15_ydu6b".+?</a>', str(sec))
            b_link = re.sub(r'<a class="_15_ydu6b" href="', '', str(a_link), flags=re.MULTILINE)
            c_link = re.sub(r'" target="_blank">.+?</a>', '', str(b_link), flags=re.MULTILINE)
            d_link = 'https://www.tripadvisor.com' + c_link.replace("'", "").replace("[", "").replace("]", "")
            counter = counter + 1
            print(counter,'  ',d_link)
            df1 = df1.append(res_info(d_link, str(name[i])))
            df2 = df2.append(res_website(d_link))

df1.to_csv('D:\\modules\\Exsell\\Exsell_Programming\\df1_'+str(i)+'.csv')
df2.to_csv('D:\\modules\\Exsell\\Exsell_Programming\\df2_'+str(i)+'.csv')