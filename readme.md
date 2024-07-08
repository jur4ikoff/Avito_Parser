# Парсер Авито

## Основные возможности
- Парсинг основной информации об объявлении (название, цена, срок, оценки владельца)

## Как запустить: 
Устанавливаем нужные библиотеки из `requirements.txt`  
Скачиваем Chrome Web Driver  
Кастомизируем файл settings  
Запустить файл гun_parser

## Версия 0.1 _Рефакторинг_
Разрабатывается консольная версия  
- Добавлено время парсинга для дальнейшей обработки
- Добавлен settings.ini
- Добавлен gitignore
- Код очищен от мусора
- Добавлен файл для запуска парсера
- Фикс бага с ранним выхода из парса
- Итоговый файл теперь называется также, как поисковый запрос

## Версия 0.0 _Начало разработки_
Разрабатывается консольная версия  
- написан парсер, который собирает данные по url в csv файл


## Роадмап
- Добавить Url объявления
- Сделать консольную версию по красоте
- Перевести парсер на selenuimbase
- Сделать веб версию
