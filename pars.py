import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import urllib
from collections import namedtuple
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import os
import configparser


def process_price(price: str) -> str:
    """Функция обрабатывает цену товара под нужный формат"""
    price = price.replace("&nbsp;", "").replace("\xa0", "")[:-1]
    return price


def process_time(time: str) -> str:
    """Функция обрабатывает время публикации объявления"""
    if "назад" in time:
        if "дней" in time or "дня" in time or "день" in time:
            return str(int(time[:2]))
        elif "минуту" in time or "минут" in time:
            return "1"
        elif "часов" in time or "час" in time:
            return "1"
        elif "недели" in time or "неделю" in time:
            return str(int(time[0]) * 7)
    return "40"


class AvitoParser:
    """Парсит объявления по url в csv файл"""

    def __init__(self, search_term: str, base_url: str, selenium_path: str):
        self.search_term = search_term
        self.base_url = base_url
        self.Ads = namedtuple("Ads", ["name", "price", "period_days", "count_marks", "avg_mark", "pars_time"])
        self.ads_list = []

        flag = True
        page = 1
        while flag:
            self.url = self.get_url(self.base_url, self.search_term, page)  # Хардкод
            page += 1
            res = self.__download_page(self.url, selenium_path)
            if res:
                parse_status = self.__parse_page()
                if parse_status:
                    print("Парс удачный")
                    time.sleep(10)
                else:
                    print("Парс страницы неудачный")
                # print("Парс удачный")
            else:
                print("Бан по Ip или неожиданный выход из селениума")
                break
            break
        self.__write_file("test.csv")

    @staticmethod
    def get_url(base_url: str, query: str, page: int) -> str:
        """Генерирует url для запроса по заданным параметрам"""
        params = {"q": query, "p": page}
        # Кодирование параметров запроса
        query_string = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_string}"
        return url

    def __download_page(self, url_to_search: str, selenium_path):
        """Скачивает HTML страницу"""
        service = Service(executable_path=selenium_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(url_to_search)
        wait = WebDriverWait(self.driver, timeout=10)

        try:
            el_with_class = self.driver.find_element(By.CLASS_NAME, "styles-module-theme-rOnN1")
            wait.until(lambda d: el_with_class.is_displayed())
        except Exception as e:
            return False
        # soup = BeautifulSoup(driver.page_source, "lxml")
        # print(self.driver.page_source)
        print(self.driver.page_source, file=open("temp.html", "a", encoding="utf-8"))
        return True

    def __parse_page(self):
        soup = BeautifulSoup(self.driver.page_source, features="lxml")
        products = soup.find_all("div", class_="iva-item-content-rejJg")

        all_read = 0
        for product in products:
            all_read += 1

            product_name = product.find("div", class_="iva-item-title-py3i_")
            # print(ad_name)
            product_cost = product.find("strong", class_="styles-module-root-bLKnd")
            price = process_price(product_cost.text)

            time = product.find("div", class_="iva-item-dateInfoStep-_acjp")
            time = process_time(time.text)

            try:
                data_marker = product.find("div", class_="SellerRating-root-v0rhv")
                rating = float(data_marker.text[:3].replace(",", "."))
                marks_count = int("".join(data_marker.text[3:].split(" ")[:-1]))
            except AttributeError as e:
                rating = 0
                marks_count = 0
            parse_time = datetime.now().strftime("%Y-%m-%d")
            product_properties = self.Ads(product_name.text, price, time, marks_count, rating, parse_time)
            self.ads_list.append(product_properties)
        if all_read > 0:
            return True
        else:
            return False

    def __write_file(self, filename: str):
        exist = False
        if os.path.exists(filename):
            exist = True

        with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            if not exist:
                writer.writerow(self.Ads._fields)

            # запись данных
            for ad in self.ads_list:
                try:
                    writer.writerow(ad)
                except Exception as e:
                    print(ad)


def config_parser():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    parse_url = config.get("Avito", "base_url")
    selenium_path = config.get("Avito", "selenium_path")
    search_term = config.get("Avito", "search_term")
    print(parse_url, selenium_path, search_term)
    parser = AvitoParser(search_term, parse_url, selenium_path)
    return parser


def start_parser():
    parser = config_parser()


if __name__ == "__main__":
    start_parser()

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

"""
file = open("temp.html", "r", encoding="utf-8")
f = file.read()"""

"""response = requests.get(url, headers=headers, allow_redirects=false)
print(response.status_code)
soup = beautifulsoup(response.text, "html.parser")
print(response.text, file=open("temp.html", 'w', encoding='utf-8'))
# parent = soup.find("div", {"class": "iva-item-body-kluuy"})
# print(parent.)

# iva-item-body-kluuy
"""
