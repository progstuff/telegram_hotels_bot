import requests
import json
from config_data.config import RAPID_API_KEY


def send_data_to_server(url, params, headers):
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == requests.codes.ok:
            return response
        print('Ошибка', response.status_code)
        return None
    except requests.ConnectionError:
        print('Ошибка соединения')
        return None


def get_lowprice_hotels(town):
    return get_hotels(town, '2022-08-20', '2022-08-21', 'PRICE')


def get_hotels(town: str, date_in: str, date_out: str, sort_rule: str):
    is_finded, locations = get_locations_from_server(town)

    if is_finded:
        town_id = locations[0][0]
        is_finded, hotels = get_hotels_from_server(town_id, date_in, date_out, sort_rule)

        return is_finded, hotels

    return False, None


def get_hotels_from_server(town_id: str, date_in: str, date_out: str, sort_rule: str):
    """
    получает отели в выбранной локации
    """
    url = 'https://hotels4.p.rapidapi.com/properties/list'
    params = {
        'destinationId': town_id,
        'pageNumber': '1',
        'pageSize': '10',
        'checkIn': date_in,
        'checkOut': date_out,
        'adults1': '1',
        'sortOrder': sort_rule,
        'locale': 'en_US',
        'currency': 'USD'
    }
    headers = {
        'X-RapidAPI-Key': RAPID_API_KEY,
        'X-RapidAPI-Host': 'hotels4.p.rapidapi.com'
    }
    answer = send_data_to_server(url, params, headers)
    if answer is not None:
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
    return False, None


def get_locations_from_server(town: str) -> (bool, [(str, str), (str, str), ...]):
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
    answer = send_data_to_server(url, params, headers)
    if answer is not None:
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
