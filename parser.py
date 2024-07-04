import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.service import service
from selenium.webdriver.support.wait import WebDriverWait
from collections import namedtuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import locale
import csv

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class AvitoParser:
    def __init(self):
        pass


def __parse():
    # formats = {
    #     "search_term": "apple ipad air 11"
    # }
    # search_term = "apple ipad air 11"
    # request = urllib.parse.quote_plus(formats)
    # print(request)
    base_url = 'https://www.avito.ru/moskva'
    params = {
        'q': 'apple ipad air 11',
    }

    # Кодирование параметров запроса
    query_string = urllib.parse.urlencode(params)
    url = f'{base_url}?{query_string}'
    print(url)
    return url
    service = Service(executable_path="C:\\Python\\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    # driver = webdriver.Chrome(service=service(executable_path="C:\\Python\\chromedriver.exe"))
    driver.get(url)
    wait = WebDriverWait(driver, timeout=1)
    el_with_class = driver.find_element(By.CLASS_NAME, "styles-module-theme-rOnN1")
    wait.until(lambda d: el_with_class.is_displayed())
    # soup = BeautifulSoup(driver.page_source, "lxml")
    print(driver.page_source, file=open("temp.html", 'w', encoding='utf-8'))
    driver.quit()

"""base_url = 'https://www.example.com/search'

# Параметры запроса
params = {
    'q': 'apple ipad air 11',
    'cd': '1'
}

# Кодирование параметров запроса
query_string = urllib.parse.urlencode(params)

# Полный URL с параметрами запроса
full_url = f'{base_url}?{query_string}'

print(full_url)"""

__parse()
exit(0)

"""
service = Service(executable_path="c:\\python\\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(url)

wait = WebDriverWait(driver, timeout=2)

# Ожидание, пока элемент с заданным классом станет доступен
el_with_class = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "styles-module-theme-ronn1")))

# Теперь можно использовать BeautifulSoup для парсинга страницы
soup = BeautifulSoup(driver.page_source, "lxml")

# Не забудьте закрыть драйвер, когда он больше не нужен
driver.quit()
"""

file = open("temp.html", "r", encoding='utf-8')
f = file.read()
soup = BeautifulSoup(f, features="lxml")
products_list = soup.find_all('div', class_='iva-item-content-rejJg')
Ads = namedtuple("Ads", ["name", "price", "period_days", "count_marks", "avg_mark"])
ads_list = []


def process_price(price: str) -> str:
    """Функция обрабатывает цену товара под нужный формат"""
    price = price.replace("&nbsp;", '').replace("\xa0", '')[:-1]
    return price


def process_time(time: str) -> str:
    """Функция обрабатывает время публикации объявления"""
    if 'назад' in time:
        if 'дней' in time or 'дня' in time or 'день' in time:
            return str(int(time[:2]))
        elif 'минуту' in time or 'минут' in time:
            return '1'
        elif 'часов' in time or 'час' in time:
            return '1'
        elif 'недели' in time or 'неделю' in time:
            return str(int(time[0]) * 7)
    return '40'


all_read = 0
for product in products_list:
    all_read += 1

    product_name = product.find('div', class_='iva-item-title-py3i_')
    # print(ad_name)
    product_cost = product.find('strong', class_='styles-module-root-bLKnd')
    price = process_price(product_cost.text)

    time = product.find('div', class_="iva-item-dateInfoStep-_acjp")
    time = process_time(time.text)

    try:
        data_marker = product.find('div', class_="SellerRating-root-v0rhv")
        rating = float(data_marker.text[:3].replace(',', '.'))
        marks_count = int("".join(data_marker.text[3:].split(" ")[:-1]))
    except AttributeError as e:
        rating = 0
        marks_count = 0

    product_properties = Ads(product_name.text, price, time, marks_count, rating)
    ads_list.append(product_properties)

with open('test.csv', mode='w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    # запись заголовкаAds
    writer.writerow(Ads._fields)
    # запись данных
    for ad in ads_list:
        try:
            writer.writerow(ad)
        except Exception as e:
            print(ad)

print(all_read)
"""response = requests.get(url, headers=headers, allow_redirects=false)
print(response.status_code)
soup = beautifulsoup(response.text, "html.parser")
print(response.text, file=open("temp.html", 'w', encoding='utf-8'))
# parent = soup.find("div", {"class": "iva-item-body-kluuy"})
# print(parent.)

# iva-item-body-kluuy
"""
