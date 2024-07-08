"""Запускает парсер по поисковому запросу"""
import configparser
from avito_parser import AvitoParserSearchTerm


def config_parser():
    """Функция читает конфигурацию из ini файла"""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    parse_url = config.get("Avito", "base_url")
    selenium_path = config.get("Avito", "selenium_path")
    search_term = config.get("Avito", "search_term")

    return parse_url, selenium_path, search_term


def start_parser():
    """Запуск парсера"""
    parse_url, selenium_path, search_term = config_parser()
    parser = AvitoParserSearchTerm(search_term, parse_url, selenium_path)


if __name__ == "__main__":
    start_parser()
