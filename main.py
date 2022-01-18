import requests, lxml
from bs4 import BeautifulSoup
import json

url = 'https://www.etovidel.net/sights/city/moscow'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                 '(KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
}

# req = requests.get(url=url, headers=headers)
#
# with open ('index.html', 'a', encoding='utf-8') as file:
#     file.write(req.text)
elements_url = []
result = []
with open('index.html', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

elements = soup.find_all('div', class_='new_content new_content_no_common')

for item in elements:
    element_url = 'https://www.etovidel.net' + item.find('a').get('href')
    elements_url.append(element_url)

count = 0
for url in elements_url:
    count += 1
    print(f'Достопримечательность №{count}')
    try:
        req = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        element_title = soup.find('div', class_='titleAndId').find('h1').text
        print(element_title)
        element_description = soup.find('a', class_='for_gallery_box').get('title')
        element_address_list = soup.find('div', class_='cont_page').find('p').text.split(':')
        element_address = element_address_list[1].strip()
        result.append(
            {
                'name': element_title,
                'description': element_description,
                'addres': element_address
            }
        )

    except Exception as ex:
        print(ex)
        print('Ошибка')

with open('result.json', 'a', encoding='utf-8') as file:
    json.dump(result, file, indent=4, ensure_ascii=False)




