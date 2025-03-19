import json

import requests
from bs4 import BeautifulSoup
import aiohttp

URL = 'https://www.mashina.kg/'

response = requests.get(URL)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    cars = soup.find_all('div', class_='category-block-content-item')
    cars_lst = []
    for car in cars:
        name = car.find('div', class_='main-title').text.strip().replace('\n', '').replace('  ', '').replace('· ', '')
        price = car.find('span', class_='currency-1')#.text.replace(' ', '').replace('с', ''))
        if price:
            price = int(price.text.replace(' ', '').replace('с', ''))
        photo = car.find('img').get('src')
        description_resp = requests.get(URL + car.find('a').get('href'))
        try:
            description_soup = BeautifulSoup(description_resp.text, 'lxml')
            description = description_soup.find('span', class_='original').text.strip()[:50] + '...'
        except Exception:
            description = 'Нет описания'
        cars_lst.append({
            'name': name,
            'price': price,
            'photo': photo,
            'description': description
        })
    with open('cars.json', 'w', encoding='utf-8') as file:
        json.dump(cars_lst, file)

