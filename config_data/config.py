import os
from dotenv import load_dotenv, find_dotenv


def get_towns() -> [{}, {}, ...]:
    towns_data = []
    with open('geo.csv', 'r') as towns:
        towns.readline()
        for line in towns:
            data = line.split(';')
            towns_data.append(
                {
                    'country_en': data[1][1:len(data[1])-1],
                    'region_en': data[2][1:len(data[2])-1],
                    'city_en': data[3][1:len(data[3])-1],
                    'country_ru': data[4][1:len(data[4])-1],
                    'region_ru': data[5][1:len(data[5])-1],
                    'city_ru': data[6][1:len(data[6])-1],
                }
            )
    return towns_data


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

TOWNS = get_towns()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

START_COMMAND = {'command_name': 'start', 'command_description': '🚀 Начать сначала'}
HELP_COMMAND = {'command_name': 'help', 'command_description': '❓ Вывести справку'}
LOW_PRICE_COMMAND = {'command_name': 'lowprice', 'command_description': '🏨 бюджетные'}
HIGH_PRICE_COMMAND = {'command_name': 'highprice', 'command_description': '🏨 дорогие'}
BEST_DEAL_COMMAND = {'command_name': 'bestdeal', 'command_description': '🔎 поиск'}
HISTORY_COMMAND = {'command_name': 'history', 'command_description': '📜 история'}
HELP_MESSAGE = '''
Что может этот бот?

 🏨 показать топ бюджетных отелей
 🏨 показать топ дорогих отелей
 🔎 найти отель по параметрам
 📜 показать историю запросов
'''
DEFAULT_COMMANDS = [START_COMMAND, HELP_COMMAND]
CUSTOM_COMMANDS = [LOW_PRICE_COMMAND, HIGH_PRICE_COMMAND, BEST_DEAL_COMMAND, HISTORY_COMMAND]
