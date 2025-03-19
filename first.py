import json

import requests
from bs4 import BeautifulSoup

response = requests.get('https://www.kivano.kg/mobilnye-telefony')

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'lxml')
    phones = soup.find_all('div', class_='item product_listbox oh')
    lst_phones = []
    for phone in phones:
        name = phone.find('div', class_='listbox_title oh').text.strip()
        price = phone.find('div', class_='listbox_price text-center').text.replace(' ', '')
        photo = phone.find('img').get('src')
        lst_phones.append({
            'name': name,
            'price': price,
            'photo': photo
        })
    with open('phones.json', 'w') as file:
        json.dump(lst_phones, file)