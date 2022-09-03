import os

from dotenv import find_dotenv, load_dotenv


def get_towns() -> [{}, {}, ...]:
    towns_data = []
    with open('geo.csv', 'r', encoding='cp1251') as towns:
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

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
TOWNS = get_towns()
START_COMMAND = {'command_name': 'start', 'command_description': '🚀 Начать сначала'}
HELP_COMMAND = {'command_name': 'help', 'command_description': '❓ Вывести справку'}

LOW_PRICE_COMMAND = {'command_name': 'lowprice',
                     'command_description': '🏨 бюджетные отели',
                     'command_welcome_mes': 'Вы выбрали показать топ бюджетных отелей в городе',
                     'image_dialog_key': 'lowprice_image_choose',
                     'image_pages_number_key': 'lowprice_image_pages_number',
                     'hotels_pages_number_key': 'lowprice_hotel_pages_number',
                     'hotels_kbrd_page_key': 'lowprice_page',
                     'image_kbrd_page_key': 'lowprice_image',
                     'town_choose_kbrd_key': 'town_lowprice'}

HIGH_PRICE_COMMAND = {'command_name': 'highprice',
                      'command_description': '🏨 дорогие отели',
                      'command_welcome_mes': 'Вы выбрали показать топ дорогих отелей в городе',
                      'image_dialog_key': 'highprice_image_choose',
                      'image_pages_number_key': 'highprice_image_pages_number',
                      'hotels_pages_number_key': 'highprice_hotel_pages_number',
                      'hotels_kbrd_page_key': 'highprice_page',
                      'image_kbrd_page_key': 'highprice_image',
                      'town_choose_kbrd_key': 'town_highprice'
                      }

BEST_DEAL_COMMAND = {'command_name': 'bestdeal',
                     'command_description': '🔎 поиск отелей',
                     'command_welcome_mes': 'Вы выбрали поиск отелей по параметрам',
                     'image_dialog_key': 'bestdeal_image_choose',
                     'image_pages_number_key': 'bestdeal_image_pages_number',
                     'hotels_pages_number_key': 'bestdeal_hotel_pages_number',
                     'hotels_kbrd_page_key': 'bestdeal_page',
                     'image_kbrd_page_key': 'bestdeal_image',
                     'town_choose_kbrd_key': 'town_bestdeal',
                     'hotels_price_key': 'hotels_price_bestdeal',
                     'distance_key': 'distance_bestdeal'
                     }

HISTORY_COMMAND = {'command_name': 'history',
                   'command_description': '📜 история',
                   'command_welcome_mes': 'Вы выбрали показать историю',
                   'hotels_pages_number_key': 'history_hotel_pages_number'}

HELP_MESSAGE = '''
Что может этот бот?

 🏨 показать топ бюджетных отелей
 🏨 показать топ дорогих отелей
 🔎 найти отель по параметрам
 📜 показать историю запросов
'''

DEFAULT_COMMANDS = [START_COMMAND, HELP_COMMAND]
CUSTOM_COMMANDS = [LOW_PRICE_COMMAND, HIGH_PRICE_COMMAND, BEST_DEAL_COMMAND, HISTORY_COMMAND]

