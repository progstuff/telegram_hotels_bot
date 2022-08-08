import requests

class TestQuerries:
    """ класс для тестовых запросов, чтобы разобраться как что работает"""
    def __init__(self):
        self.__rapid_api_key = '7cdcd41828msh59dda980b1b10a0p1c050ajsn10e4bc3f5d43'
        self.__bot_token = '5494477157:AAHOTYk_NgIUYVJmUNJZ0-u850FdmFAniis'

    def try_get_data_from_rapid(self) -> str:
        """ тест работы с rapidapi """
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
            отправляет стандартный
        """
        url = 'https://api.telegram.org/bot{bot_token}/getMe'.format(bot_token=self.__bot_token)
        answer = requests.get(url)
        return answer.text
