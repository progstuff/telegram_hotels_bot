import json
from utils.misc.rapid_api_utils  import get_lowprice_hotels


class Hotel:
    def __init__(self):
        self.__id = 0
        self.__name = ''
        self.__address = ''
        self.__center_dist = ''

    def set_hotel_data(self, hotel):
        self.__id = hotel.get('id', None)
        self.__name = hotel.get('name', None)
        adr = hotel.get('address')
        if type(adr) is dict:
            self.__address = ', '.join([adr.get('locality', ''), adr.get('streetAddress', '')])
        landmarks = hotel.get('landmarks')
        if type(landmarks) is list:
            if landmarks[0].get('label', '') == 'City center':
                self.__center_dist = landmarks[0].get('distance', '')

    def get_str_view(self):
        rez = '\n'.join([self.__name, self.__address, self.__center_dist])
        return rez


def get_lowprice_data_from_server():
    is_success, hotels = get_lowprice_hotels('new york')
    if is_success:
        with open('lowprice_result.json', 'w') as file:
            json.dump(hotels, file, indent=4)
            #bot.send_message(message.from_user.id, hotel_cl.get_str_view())
    print(hotels)

def get_lowprice_hotel_data(ind):
    with open('lowprice_result.json', 'r') as file:
        data = json.load(file)
    if len(data) > ind+1:
        h = Hotel()
        h.set_hotel_data(data[ind])
        return h.get_str_view()
    return ''