from loader import bot
from telebot.types import Message
from config_data.config import LOW_PRICE_COMMAND
from config_data.config import RAPID_API_KEY
import requests
import json


@bot.message_handler(commands=[LOW_PRICE_COMMAND['command_name']])
def lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id, 'вы выбрали показать топ самых дешевых отелей в городе. Введите город')
    is_success, hotels = get_hotels('new york')
    if is_success:
        with open('result.json', 'w') as file:
            json.dump(hotels, file, indent=4)
    print(hotels)


@bot.message_handler(content_types='text')
def lowprice_button_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description']:
        lowprice(message)


def get_hotels(town):
    is_finded, locations = get_locations_from_server('new york')

    if is_finded:
        town_id = locations[0][0]
        is_finded, hotels = get_hotels_from_server(town_id)

        return is_finded, hotels

    return False, None


def get_hotels_from_server(town_id: str):
    """
    получает отели в выбранной локации
    """
    url = 'https://hotels4.p.rapidapi.com/properties/list'
    params = {
        'destinationId': town_id,
        'pageNumber': '1',
        'pageSize': '10',
        'checkIn': '2022-08-13',
        'checkOut': '2022-08-15',
        'adults1': '1',
        'sortOrder': 'PRICE',
        'locale': 'en_US',
        'currency': 'USD'
    }
    headers = {
        'X-RapidAPI-Key': RAPID_API_KEY,
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }
    answer = requests.get(url, params=params, headers=headers)
    hotels_info = json.loads(answer.text)

    data = hotels_info.get('data', None)
    if data is None:
        return False, None

    body = data.get('body', None)
    if body is None:
        return False, None

    search_results = body.get('searchResults', None)
    if search_results is None:
        return False, None

    hotels = search_results.get('results', None)
    return True, hotels



def get_locations_from_server(town: str)  -> (bool, [(str, str)]):
    """
    получает локации от сервера, локациями считаются только города
    """
    url = 'https://hotels4.p.rapidapi.com/locations/v2/search'
    params = {
        'query': town,
        'locale': 'en_US',
        'currency': 'USD'
    }
    headers = {
        'X-RapidAPI-Key': RAPID_API_KEY,
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }
    answer = requests.get(url, params=params, headers=headers)
    locations = json.loads(answer.text)

    if len(locations) > 0:
        group_finded = False
        for location in locations.get("suggestions"):
            group = location.get("group", None)
            if group == "CITY_GROUP":
                group_finded = True
                break

        if group_finded:
            places = location.get('entities', None)
            if places is not None:
                return True, [(place.get('destinationId'), place.get('name')) for place in places if place.get("type", "") == "CITY"]
    return False, None
