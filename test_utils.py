import requests
import telebot
class TestQuerries:
    """ класс для тестовых запросов, чтобы разобраться как что работает """
    def __init__(self):
        self.__rapid_api_key = '7cdcd41828msh59dda980b1b10a0p1c050ajsn10e4bc3f5d43'
        self.__bot_token = '5494477157:AAHOTYk_NgIUYVJmUNJZ0-u850FdmFAniis'

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
