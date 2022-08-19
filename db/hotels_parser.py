from utils.misc.rapid_api_utils  import get_lowprice_hotels, get_images_links

hotels_data = {}


class Hotel:
    def __init__(self, hotel_data):
        self.__id = 0
        self.__name = ''
        self.__address = ''
        self.__center_dist = ''
        self.__links = []
        self.set_hotel_data(hotel_data)

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

    @property
    def links(self):
        return self.__links

    @links.setter
    def links(self, new_links):
        self.__links = new_links[:]

    @property
    def id(self):
        return self.__id

    def get_str_view(self):
        rez = '\n'.join([self.__name, self.__address, self.__center_dist])
        return rez


def get_images_links_from_server(chat_id):
    hotels = hotels_data
    for hotel in hotels[chat_id]:
        hotel_id = hotel.id
        is_success, links = get_images_links(hotel_id)
        if is_success:
            hotel.links = links


def get_lowprice_data_from_server(chat_id):
    is_success, hotels = get_lowprice_hotels('new york')
    if is_success:
        hotels_data[chat_id] = []
        for hotel in hotels:
            hotels_data[chat_id].append(Hotel(hotel))
        return len(hotels)
    return 0
    print(hotels)




def get_hotel_id(chat_id, ind):
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if ind <= len(data):
            return data[ind-1].id
    return None


def get_hotel_image(chat_id, hotel_ind, image_ind):
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if hotel_ind <= len(data):
            links = data[hotel_ind - 1].links
            if len(links) >= image_ind:
                return links[image_ind - 1]
    return None


def get_lowprice_hotel_data(chat_id, ind):
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if ind <= len(data):
            return data[ind - 1].get_str_view()
    return ''