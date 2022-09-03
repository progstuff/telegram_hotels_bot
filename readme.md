# hoteIsBot
## телеграмм бот для просмотра отелей

бот может:

- показать топ бюджетных отелей
- показать топ дорогих отелей
- выполнить поиск отелей по параметрам
- показать историю просмотренных отелей

## Установка

для установки бота необходимо:
- клонировать репозиторий командой:
```sh
git clone https://gitlab.skillbox.ru/andrei_morozov_3/python_basic_diploma.git
```
- установить библиотеки из файла requirements.txt:
```sh
pip install pyTelegramBotAPI==4.6.1
pip install python-dotenv==0.20.0
pip install requests==2.28.1
pip install telebot==0.0.4
pip install python-telegram-bot-pagination==0.0.2
pip install python-telegram-bot-calendar==1.0.5
pip install peewee==3.15.2
pip install isort==5.10.1
pip install loguru==0.6.0
```
- создать файл .env со структурой как указано в env.template и указать ключ для rapid api и токен телеграм бота (с кавычками)
 ```sh
RAPID_API_KEY = "rapid api key"
BOT_TOKEN = "telegram bot token"
```
## Использование
Для взаимодействия с ботом используются команды: /lowprice, /highprice, /bestdeal, /history, /start
Команды можно вводить вручную или выбрать в меню, будет запущен соответствующий диалог
![alt text](https://gitlab.skillbox.ru/andrei_morozov_3/python_basic_diploma/-/tree/history-func/screenshots/menu.png?raw=true)
Также при выборе команды /start предлагается запуск одного из диалогов
![alt text](https://gitlab.skillbox.ru/andrei_morozov_3/python_basic_diploma/-/tree/history-func/screenshots/menu2.png?raw=true)
После ввода всех необходимых данных начинается загрузка отелей
![alt text](https://gitlab.skillbox.ru/andrei_morozov_3/python_basic_diploma/-/tree/history-func/screenshots/hotels.png?raw=true)
При выборе команды /history будет загружена история с ранее просмотренными отелями
![alt text](https://gitlab.skillbox.ru/andrei_morozov_3/python_basic_diploma/-/tree/history-func/screenshots/history.png?raw=true)


