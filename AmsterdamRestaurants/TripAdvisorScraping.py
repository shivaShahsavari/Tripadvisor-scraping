import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time
from selenium import webdriver

####################Gathering links of restaurants in TripAdvisor##########################################
def restaurant_links():
    res_links=[]
    headers = {"Accept-Language": "en-US, en;q=0.5", 'User-agent': 'Super Bot 9000'}

    next_link=['https://www.tripadvisor.com/Restaurants-g188590-oa3870-Amsterdam_North_Holland_Province.html#EATERY_LIST_CONTENTS']
    for i in range(130):## edition for Generalization
        a='https://www.tripadvisor.com/Restaurants-g188590-oa'+str(30*i)+'-Amsterdam_North_Holland_Province.html#EATERY_LIST_CONTENTS'
        next_link.append(a)

    for i in range(1,len(next_link)):
        results = requests.get(next_link[i-1], headers=headers)  
        soup = BeautifulSoup(results.text, "html.parser")
        for sec in soup.find_all('div', class_="_1llCuDZj"):
            a_link=re.findall('<a class="_15_ydu6b".+?</a>',str(sec))
            b_link=re.sub(r'<a class="_15_ydu6b" href="', '', str(a_link), flags=re.MULTILINE)
            c_link=re.sub(r'" target="_blank">.+?</a>', '', str(b_link), flags=re.MULTILINE)
            d_link='https://www.tripadvisor.com'+c_link.replace("'","").replace("[","").replace("]","")
            res_links.append(d_link)

    pd.DataFrame(res_links,columns=['Links']).to_csv('D:\\modules\\Exsell\\Exsell_Programming\\res_links_v1.csv')
    print('Number of restaurant Links: ',len(res_links))

##Note : Splitting file of links into files with 600 records & then calling them to extract data

def data_split():

    path = "D:\\modules\\Exsell\\Exsell_Programming\\res_links_v1.csv" # path to file
    df = pd.read_csv(path) # reading file
    low = 0 # Initial Lower Limit
    high = 600 # Initial Higher Limit
    i=0
    print(len(df))
    while(high < len(df)):
        df_new = df[low:high] # subsetting DataFrame based on index
        low = high+1 #changing lower limit
        high = high + 599 # givig uper limit with increment of 1000
        df_new.to_csv('D:\\modules\\Exsell\\Exsell_Programming\\res_links_v1_'+str(i)+'.csv',columns=['Links']) # output file
        i=i+1
    df_new = df[low:len(df)]
    df_new.to_csv('D:\\modules\\Exsell\\Exsell_Programming\\res_links_v1_'+str(i)+'.csv',columns=['Links'])

    print("Splitting data into chunks of 600 rows are done")

################################ Scraping each link & Extracting specified data ############################
def res_info():  
    column_names=['Name','TripAdvisorLink','status','pricestatus','adress','city','phone','email','website','rating','reviews','subcat','detail','Thuisbezorgd','TheFork']
    res_info=pd.DataFrame(columns=column_names)
    user_agent_old_phone = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    res_header={'User-Agent': user_agent_old_phone}
    for j in range(8):## edition for Generalization
        print('round : ',j)
        df=pd.read_csv(r"D:\\modules\\Exsell\\Exsell_Programming\\res_links_v1_"+str(j)+".csv",header=0)
        print('file name : res_links_',str(j))
        res_info=pd.DataFrame(columns=column_names)
        for l in range(len(df)):
            results_res = requests.get(df['Links'][l], headers=res_header)
            soup_res = BeautifulSoup(results_res.text, "html.parser")
            link=df['Links'][l]
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
            'adress': address if address else 'N','city':'Amsterdam','phone':phone if phone else 'N','email':' ','website':' ',
            'pricestatus':priceStatus if priceStatus else 'N','rating':overallRating if overallRating else 'N',
            'reviews':reviews if reviews else 'N', 'subcat':subcat if subcat else 'N','detail':detail if detail else detail1,
            'Thuisbezorgd':'True' if delivery else 'False','TheFork':'True' if reserve else 'False'}, ignore_index=True)
            print(l)
        res_info.to_csv('D:\\modules\\Exsell\\Exsell_Programming\\res_info_'+str(j)+'.csv')
        time.sleep(30)
    print("done")

#######################################
def res_website(): 
    column_names=['Name','TripAdvisorLink','website','email']
    user_agent_old_phone = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    res_header={'User-Agent': user_agent_old_phone}
    driver = webdriver.Chrome('C:\\chromedriver_win32\\chromedriver.exe') 
    for i in (7,8):
        print('round : ',i)
        df=pd.read_csv(r"D:\\modules\\Exsell\\Exsell_Programming\\res_links_v1_"+str(i)+".csv",header=0)
        print('file name : res_links_',str(i))
        res_web=pd.DataFrame(columns=column_names)
        for l in range(len(df)):
            results_res = requests.get(df['Links'][l], headers=res_header)
            soup_res = BeautifulSoup(results_res.text, "html.parser")
            link=df['Links'][l]
            website1=email=Name=''
            try:    
                Name=soup_res.find('h1',class_="_3a1XQ88S").text
                driver.get(df['Links'][l])
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
            print(l)
        res_web.to_csv('D:\\modules\\Exsell\\Exsell_Programming\\res_info_website_'+str(i)+'.csv')
        time.sleep(30)
    print("done")

########################## Collecting each file consisting of scraped data together ##########################

columns_res=['Unnamed: 0','Name','TripAdvisorLink','status','pricestatus','adress','city','phone','email','website',
'rating','reviews','subcat','detail','Thuisbezorgd','TheFork']
def collect_restuarant():
    res=pd.DataFrame(columns=columns_res)
    for i in range(8):
        df_res=pd.read_csv(r"D:\\modules\\Exsell\\Exsell_Programming\\res_info_"+str(i)+".csv",encoding = "UTF-8",header=0)
        df_web=pd.read_csv(r"D:\\modules\\Exsell\\Exsell_Programming\\res_info_website_"+str(i)+".csv",encoding = "UTF-8",header=0)
        for j in range(len(df_res)):
            df_res['email'][j]=df_web['email'][j]
            df_res['website'][j]=df_web['website'][j]
        res=res.append(df_res)
    return res

################################################ Main body ###################################################

restaurant_links()
print('Aggregation of links is done')
data_split()
res_website()
print('Scraping web and emails is done')
res_info()
print('Scraping data of links is done')
res_seg=pd.DataFrame(columns=columns_res)
res_seg=collect_restuarant()
print('the shape of restaurant segment is ',res_seg.shape)
res_seg.to_csv("D:\\modules\\Exsell\\Exsell_Programming\\restaurant_TripAdvisor_Amsterdam.csv")





