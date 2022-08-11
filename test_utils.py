import requests
import telebot
import os
from os.path import join, dirname
from dotenv import load_dotenv
class TestQuerries:
    """ класс для тестовых запросов, чтобы разобраться как что работает """
    def __init__(self):
        """загрузка ключа и токена из файла .env"""
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.__rapid_api_key = os.getenv('RAPID_API_KEY')
        self.__bot_token = os.getenv('BOT_TOKEN')

    def try_get_data_from_rapid(self) -> str:
        """
            тест работы с rapidapi
            возвращает текст ответа
        """
        url = 'https://hotels4.p.rapidapi.com/locations/v2/search'
        params = {
            'query': 'new york',
            'locale': 'en_US',
            'currency': 'USD'
        }
        headers = {
            'X-RapidAPI-Key': self.__rapid_api_key,
            'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
        }
        answer = requests.get(url, params=params, headers=headers)
        return answer.text

    def try_get_data_from_bot(self) -> str:
        """
        тест работы с телеграмм ботом
        возвращает текст ответа
        """
        url = 'https://api.telegram.org/bot{bot_token}/getMe'.format(bot_token=self.__bot_token)
        answer = requests.get(url)
        return answer.text

    def start_echo_bot(self) -> None:
        """
            пример из документации эхо-бота
            в ответ на команды /start /help отправляет сообщение Howdy, how are you doing?
            в ответ на другие любые сообщения - дублирует их в чате
        """
        bot = telebot.TeleBot(self.__bot_token)

        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.reply_to(message, "Howdy, how are you doing?")

        @bot.message_handler(func=lambda message: True)
        def echo_all(message):
            bot.reply_to(message, message.text)

        bot.infinity_polling()

    def start_diploma_bot(self) -> None:
        """
        ссылка на бота t.me/hoteIs_heIper_bot
        запускает бот с основными командами:
        /help
        /lowprice
        /highprice
        /bestdeal
        /history
        """
        bot = telebot.TeleBot(self.__bot_token)

        @bot.message_handler(commands=['help'])
        def send_help(message: str) -> None:
            bot.reply_to(message, "здесь будет помощь по командам")
            print('пришёл запрос на показ помощи по командам')

        @bot.message_handler(commands=['lowprice'])
        def send_lowprice(message: str) -> None:
            bot.reply_to(message, "здесь будут показаны самые дешёвые отели города")
            print('пришёл запрос на показ самых дешёвых отелей города')

        @bot.message_handler(commands=['highprice'])
        def send_highprice(message: str) -> None:
            bot.reply_to(message, "здесь будут показаны самые дорогие отели города")
            print('пришёл запрос на показ самых дорогих отелей города')

        @bot.message_handler(commands=['bestdeal'])
        def send_bestdeal(message: str) -> None:
            bot.reply_to(message, "здесь будут показаны  наиболее подходящих по цене и расположению от центра")
            print('пришёл запрос на показ наиболее подходящих по цене и расположению от центра')

        @bot.message_handler(commands=['history'])
        def send_history(message: str) -> None:
            bot.reply_to(message, "здесь будет показана история поиска отелей")
            print('пришёл запрос на показ истории')

        print('Тестовый бот запущен')
        bot.infinity_polling()

