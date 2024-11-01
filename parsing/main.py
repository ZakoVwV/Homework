import requests
from bs4 import BeautifulSoup as BS
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BS(html, 'lxml')
    phones = soup.find_all('div', class_='listbox_img pull-left')
    phone_prices = soup.find_all('div', class_='listbox_price text-center')

    data_list = []
    
    for phone, price in zip(phones, phone_prices):
        try:
            title = phone.find('img').get('alt')
        except:
            title = ''
        
        try:
            image = phone.find('img').get('src')
            image = f'https://www.kivano.kg{image}'
        except:
            image = ''
        
        try:
            price_value = price.find('strong').text.strip()
        except:
            price_value = ''

        data = {
            'phone names': title,
            'phone prices': price_value,
            'images': image
        }
        data_list.append(data)
    
    return data_list

def write_csv(data):
    with open('phones.csv', 'a', newline='', encoding='utf-8') as csv_file:
        names = ['phone names', 'phone prices', 'images']
        writer = csv.DictWriter(csv_file, delimiter='|', fieldnames=names)
        if csv_file.tell() == 0:
            writer.writeheader()
        writer.writerows(data)

def main():
    url = 'https://www.kivano.kg/mobilnye-telefony'
    html = get_html(url)
    all_data = get_data(html)  # Получаем данные с первой страницы
    
    for page in range(2, 16):
        url = f'https://www.kivano.kg/mobilnye-telefony?page={page}'
        html = get_html(url)
        all_data.extend(get_data(html))  # Добавляем данные с последующих страниц
    
    write_csv(all_data)  # Записываем все собранные данные в CSV

if __name__ == "__main__":
    main()
