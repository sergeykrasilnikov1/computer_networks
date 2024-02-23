from LxmlSoup import LxmlSoup
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'
}

url = 'https://sibverk.ru/index.php?login=yes'

data = {
    "backurl": "/index.php?login=yes",
    "AUTH_FORM": "Y",
    "TYPE": "AUTH",
    "POPUP_AUTH": "Y",
    "USER_LOGIN": "krasilnikov1967@bk.ru",
    "USER_PASSWORD": "Raincoat-1",
    "Login": "Войти"
}

session = requests.Session()
session.headers.update(headers)
response = session.post(url, data=data, headers=headers)




title_list = []
price_list = []
quantity_list = []
pages_list = []
publishing_list = []
year_list = []
paginations_pages = 66
for page in range(1, paginations_pages):
    url = f'https://sibverk.ru/catalog/knigi/fantastika-fentezi-mistika/?PAGEN_1={page}'
    response2 = session.get(url, data=data, headers=headers)
    soup = LxmlSoup(response2.text)
    links = soup.find_all('a', class_='dark_link')[28:]
    for i, link in enumerate(links):
        url = link.get("href")
        name = link.text()
        year = name.split()[-3][:-2]
        publishing = name.split()[-4][1:-1]
        price = soup.find_all("span", class_="price_value")[i].text()
        quantity = soup.find_all("span", class_="value")[i].text()
        pages = name.split()[-1]
        name = ' '.join(link.text().split()[:-4][:-1])
        title_list.append(name)
        price_list.append(price)
        quantity_list.append(quantity)
        pages_list.append(pages)
        publishing_list.append(publishing)
        year_list.append(year)

df = pd.DataFrame({'Заголовок': title_list,
    'Цена': price_list,
    'Сколько осталось':quantity_list,
    'Количество страниц':pages_list,
    'Год': year_list,
    'Издательство': publishing_list})


# Сохранение датафрейма в CSV-файл
df.to_csv('output.csv', index=False)