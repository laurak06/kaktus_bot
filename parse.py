from bs4 import BeautifulSoup
import requests


URL = 'https://kaktus.media/?lable=8&date=2025-03-17&order=time'


def parse_news():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'lxml')
        news_soup = soup.find_all('div', class_='Tag--article')[:20]
        news = {}
        for i, new in enumerate(news_soup, 1):
            title = new.find('a', class_='ArticleItem--name').text.strip()
            time = new.find('div', class_='ArticleItem--info').text.strip()
            photo = new.find('img').get('src')
            link = new.find('a', class_='ArticleItem--name').get('href')
            news[i] = {
                'title': title,
                'time': time,
                'photo': photo,
                'link': link
            }
        return news
    except requests.exceptions.HTTPError:
        return None


def parse_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        desc = soup.find('div', class_='BbCode')
        desc = desc.find('p').text + desc.find('p').text
        return desc
    except:
        return "Нет описания"
