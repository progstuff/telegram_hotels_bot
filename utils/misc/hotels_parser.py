from datetime import date

from utils.misc.rapid_api_utils import get_filtered_hotels, get_images_links


class Hotel:
    def __init__(self, hotel_data: dict, date_in: date, date_out: date):
        self.__id = 0
        self.__name = ''
        self.__address = ''
        self.__center_dist = ''
        self.__price = ''
        self.__price_total = ''
        self.__links = []
        self.__hotel_link = ''
        self.__total_cost = 0
        self.__exact_current = 0
        self.__days_cnt = 0
        self.set_hotel_data(hotel_data)
        self.calculate_total_cost((date_out - date_in).days)

    def calculate_total_cost(self, days_number: int):
        self.__days_cnt = days_number
        self.__total_cost = self.__exact_current * days_number

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
                exact_price = price.get('exactCurrent', None)
                if exact_price is not None:
                    self.__exact_current = exact_price

    @property
    def exact_current(self) -> str:
        return self.__exact_current

    @property
    def hotel_link(self) -> str:
        return self.__hotel_link

    @property
    def name(self) -> str:
        return self.__name

    @property
    def address(self) -> str:
        return self.__address

    @property
    def center_dist(self) -> str:
        return self.__center_dist

    @property
    def price(self) -> str:
        return self.__price

    @property
    def total_cost(self) -> float:
        return self.__total_cost

    @property
    def days_cnt(self) -> int:
        return self.__days_cnt

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
        rez = '\n'.join(["отель: {}".format(self.__name),
                         "адрес: {}".format(self.__address),
                         "расстояние до центра: {}".format(self.__center_dist),
                         "цена за ночь: {}$".format(int(round(self.__exact_current))),
                         "число ночей: {}".format(self.__days_cnt),
                         "суммарная стоимость: {0}$".format(int(round(self.__total_cost))),
                         "страница отеля: {}".format(self.__hotel_link)])
        return rez