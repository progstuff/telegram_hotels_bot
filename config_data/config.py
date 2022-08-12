import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

START_COMMAND = {'command_name': 'start', 'command_description': '🚀 Запустить бот'}
HELP_COMMAND = {'command_name': 'help', 'command_description': '❓ Вывести справку'}
LOW_PRICE_COMMAND = {'command_name': 'lowprice', 'command_description': '🏨 бюджетные'}
HIGH_PRICE_COMMAND = {'command_name': 'highprice', 'command_description': '🏨 дорогие'}
BEST_DEAL_COMMAND = {'command_name': 'bestdeal', 'command_description': '🔎 поиск'}
HISTORY_COMMAND = {'command_name': 'history', 'command_description': '📜 история'}
HELP_MESSAGE = '''
Что может этот бот?\n

 🏨 показать топ бюджетных отелей \n
 🏨 показать топ дорогих отелей \n
 🔎 найти отель по параметрам\n
 📜 показать историю запросов
'''
DEFAULT_COMMANDS = [START_COMMAND, HELP_COMMAND]
CUSTOM_COMMANDS = [LOW_PRICE_COMMAND, HIGH_PRICE_COMMAND, BEST_DEAL_COMMAND, HISTORY_COMMAND]