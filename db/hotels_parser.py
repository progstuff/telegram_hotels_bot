from utils.misc.rapid_api_utils  import get_filtered_hotels, get_images_links

hotels_data = {}


class Hotel:
    def __init__(self, hotel_data: dict):
        self.__id = 0
        self.__name = ''
        self.__address = ''
        self.__center_dist = ''
        self.__price = ''
        self.__price_total = ''
        self.__links = []
        self.__hotel_link = ''
        self.set_hotel_data(hotel_data)

    def set_hotel_data(self, hotel: dict) -> None:
        self.__id = hotel.get('id', None)
        self.__hotel_link = "https://www.hotels.com/ho{}".format(self.__id)
        self.__name = hotel.get('name', None)
        adr = hotel.get('address')
        if type(adr) is dict:
            self.__address = ', '.join([adr.get('locality', ''), adr.get('streetAddress', '')])
        landmarks = hotel.get('landmarks')
        if type(landmarks) is list:
            if landmarks[0].get('label', '') == 'City center':
                self.__center_dist = landmarks[0].get('distance', '')
        rate_plan = hotel.get('ratePlan', None)
        if rate_plan is not None:
            price = rate_plan.get("price", None)
            if price is not None:
                price_current = price.get('current', None)
                if price_current is not None:
                    self.__price = price_current
                price_total = price.get('fullyBundledPricePerStay', None)
                if price_total is not None:
                    self.__price_total = price_total

    @property
    def links(self) -> str:
        return self.__links

    @links.setter
    def links(self, new_links: list) -> None:
        self.__links = new_links[:]

    @property
    def id(self) -> int:
        return self.__id

    def get_str_view(self) -> str:
        rez = '\n'.join(["отель {}".format(self.__name),
                         "адрес: {}".format(self.__address),
                         "расстояние до центра {}".format(self.__center_dist),
                         "цена за ночь {}".format(self.__price),
                         "ссылка на отель: {}".format(self.__hotel_link)])
        return rez


def get_images_links_from_server(hotel: dict, max_images_cnt: int) -> int:
    hotel_id = hotel.id
    is_success, links = get_images_links(hotel_id, max_images_cnt)
    if is_success:
        hotel.links = links
        return len(links)
    return 0


def get_hotel_data_from_server(chat_id: int, town: str, max_pages_cnt: int, filter_value: str) -> int:
    is_success, hotels = get_filtered_hotels(town, max_pages_cnt, filter_value)
    if is_success:
        hotels_data[chat_id] = []
        for hotel in hotels:
            hotels_data[chat_id].append(Hotel(hotel))
        print(hotels)
        return len(hotels)
    print('отели не получены')
    return 0


def get_hotel_id(chat_id: int, ind: int) -> int:
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if ind <= len(data):
            return data[ind-1].id
    return None


def get_hotel(chat_id: int, ind: int) -> dict:
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if ind <= len(data):
            return data[ind-1]
    return None


def get_hotel_image(chat_id: int, hotel_ind: int, image_ind: int) -> str:
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if hotel_ind <= len(data):
            links = data[hotel_ind - 1].links
            if len(links) >= image_ind:
                return links[image_ind - 1]
    return None


def get_lowprice_hotel_data(chat_id: int, ind: int) -> str:
    data = hotels_data.get(chat_id, None)
    if data is not None:
        if ind <= len(data):
            return data[ind - 1].get_str_view()
    return ''