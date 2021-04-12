import requests
from bs4 import BeautifulSoup
import pandas as pd

# For all the pages
city = []
weblink = []
URL = 'https://www.tripadvisor.com/Restaurants-g188553-oa10-The_Netherlands.html#LOCATION_LIST'
links = [URL]
for i in range(1,79):
    urls = 'https://www.tripadvisor.com/Restaurants-g188553-oa'+str(20*i)+'-The_Netherlands.html#LOCATION_LIST'
    links.append(urls)
for i in range(len(links)):
    if i == 0:
        page = requests.get(links[i])
        soup = BeautifulSoup(page.content, 'lxml')
        for match in soup.find_all('div', class_='geo_name'):
            name = match.a.text
            link = match.a.attrs['href']
            link = 'https://www.tripadvisor.com' + link
            city.append(name)
            weblink.append(link)
    else:
        page = requests.get(links[i])
        soup = BeautifulSoup(page.content, 'lxml')
        match = soup.find('div', class_='deckB')
        links2 = match.find_all('li')

        for l in links2:
            province = l.find('span', class_='state').get_text()
            name = l.a.text
            link = l.a.attrs['href']
            link = 'https://www.tripadvisor.com' + link
            city.append(name)
            weblink.append(link)

df = pd.DataFrame(columns=['city','link'])
df.city = city
df.link = weblink
df.to_csv('citylinks.csv')

