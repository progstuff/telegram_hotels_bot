from datetime import date, timedelta
from utils.misc.hotels_parser import Hotel
from utils.misc.rapid_api_utils import get_filtered_hotels
from database.db_class_data import CommandDataDb, HotelDb, CommandHotelsDb, convert_datetime_field_to_date

class LocalHotelsStorage:

    def __init__(self):
        self.__hotels_data = []

    def get_hotels_cnt(self):
        return len(self.__hotels_data)

    def get_images_links_from_server(self, hotel_ind, max_images_cnt: int) -> int:
        hotel = self.get_hotel(hotel_ind)
        hotel_id = hotel.id
        is_success, links = self.get_images_links(hotel_id, max_images_cnt)
        if is_success:
            hotel.links = links
            return len(links)
        return 0

    def get_hotel_data_from_db(self, command_id, page_ind, page_size) -> int:
        com_data = CommandDataDb.get(CommandDataDb.id == command_id)
        hotels = HotelDb.select().join(CommandHotelsDb).where(CommandHotelsDb.command_data == com_data)
        self.__hotels_data = []
        start_ind = (page_ind - 1)*page_size
        end_ind = start_ind + page_size-1
        start_date = convert_datetime_field_to_date(com_data.date_in)
        end_date = convert_datetime_field_to_date(com_data.date_out)
        for ind in range(start_ind, end_ind + 1):
            self.__hotels_data.append(Hotel.get_hotel_by_db_object(hotels[ind], start_date, end_date))
        return len(self.__hotels_data)

    def get_hotel_data_from_server(self, town: str, start_date: date, end_date: date, max_pages_cnt: int,
                                   cur_global_page_ind: int, filter_value: str, min_price=None, max_price=None) -> int:
        is_success, hotels = get_filtered_hotels(town, start_date, end_date, max_pages_cnt, cur_global_page_ind,
                                                 filter_value, min_price, max_price)
        if is_success:
            self.__hotels_data = []
            for hotel in hotels:
                self.__hotels_data.append(Hotel.get_hotel_by_dict_object(hotel, start_date, end_date))
            return len(hotels)
        print('отели не получены')
        return 0

    def get_hotel_id(self, ind: int) -> int:
        data = self.__hotels_data
        if ind <= len(data):
            return data[ind - 1].id
        return None

    def get_hotel(self, ind: int) -> Hotel:
        data = self.hotels_data
        if data is not None:
            if ind <= len(data):
                return data[ind - 1]
        return None

    def get_hotel_image(self, hotel_ind: int, image_ind: int) -> str:
        data = self.hotels_data
        if hotel_ind <= len(data):
            links = data[hotel_ind - 1].links
            if len(links) >= image_ind:
                return links[image_ind - 1]
        return None

    def get_db_hotel_data(self, ind: int) -> str:
        data = self.__hotels_data
        if ind <= len(data):
            return data[ind].get_str_view()
        return ''

    @property
    def hotels_data(self):
        return self.__hotels_data


class CommandUserData:

    def __init__(self):
        self.__city_en = ''
        self.__city_ru = ''
        self.__min_price = None
        self.__max_price = None
        self.__image_choose = False
        self.__cur_image_index = 1
        self.__max_image_index = 2
        self.__cur_page_index = 1
        self.__max_page_index = 5
        self.__photo_message_id = 0
        self.__text_message_id = 0
        self.__image_choose_keyboard_message_id = 0
        self.__image_cnt_choose_keyboard_message_id = 0
        self.__town_keyboard_message_id = 0
        self.__price_keyboard_message_id = 0
        self.__distance_keyboard_message_id = 0
        self.__pages_cnt_keyboard_message_id = 0
        self.__info_message_id = 0
        self.__hotels_data = LocalHotelsStorage()
        self.__cur_global_page_ind = 1
        self.__max_global_page_ind = 1
        self.__command_db_id = 0

        cur_date = date.today()
        start_day = cur_date + timedelta(days=1)
        end_day = start_day + timedelta(days=1)
        self.__date_in = start_day
        self.__date_out = end_day

    def clear_data(self):
        self.__city_en = ''
        self.__city_ru = ''
        self.__min_price = None
        self.__max_price = None
        self.__image_choose = False
        self.__cur_image_index = 1
        self.__max_image_index = 2
        self.__cur_page_index = 1
        self.__max_page_index = 5
        #self.__photo_message_id = 0
        #self.__text_message_id = 0
        self.__image_choose_keyboard_message_id = 0
        self.__image_cnt_choose_keyboard_message_id = 0
        self.__town_keyboard_message_id = 0
        self.__price_keyboard_message_id = 0
        self.__distance_keyboard_message_id = 0
        self.__pages_cnt_keyboard_message_id = 0
        self.__info_message_id = 0
        self.__date_in = ''
        self.__date_out = ''

    def increase_global_page_ind(self):
        cur_ind = self.__cur_global_page_ind
        max_ind = self.__max_global_page_ind
        if cur_ind == max_ind:
            self.__cur_global_page_ind += 1
            self.__max_global_page_ind += 1
        else:
            self.__cur_global_page_ind += 1

    def decrease_global_page_ind(self):
        cur_ind = self.__cur_global_page_ind
        if cur_ind > 1:
            self.__cur_global_page_ind -= 1

    def reset_global_page_ind(self):
        self.__cur_global_page_ind = 1
        self.__max_global_page_ind = 1

    @property
    def city_en(self) -> str:
        return self.__city_en

    @city_en.setter
    def city_en(self, city: str):
        self.__city_en = city

    @property
    def city_ru(self) -> str:
        return self.__city_ru

    @city_ru.setter
    def city_ru(self, city: str):
        self.__city_ru = city

    @property
    def image_choose(self) -> bool:
        return self.__image_choose

    @image_choose.setter
    def image_choose(self, image_choose: bool):
        self.__image_choose = image_choose

    @property
    def max_image_index(self) -> int:
        return self.__max_image_index

    @max_image_index.setter
    def max_image_index(self, new_val: int):
        self.__max_image_index = new_val

    @property
    def cur_image_index(self) -> int:
        return self.__cur_image_index

    @cur_image_index.setter
    def cur_image_index(self, new_index: int):
        if (new_index > 0) and (new_index <= self.__max_image_index):
            self.__cur_image_index = new_index

    @property
    def cur_page_index(self) -> int:
        return self.__cur_page_index

    @cur_page_index.setter
    def cur_page_index(self, page_index: int):
        self.__cur_page_index = page_index

    @property
    def max_page_index(self) -> int:
        return self.__max_page_index

    @max_page_index.setter
    def max_page_index(self, page_cnt: int):
        self.__max_page_index = page_cnt

    @property
    def photo_message_id(self) -> int:
        return self.__photo_message_id

    @photo_message_id.setter
    def photo_message_id(self, new_id: int):
        self.__photo_message_id = new_id

    @property
    def text_message_id(self) -> int:
        return self.__text_message_id

    @text_message_id.setter
    def text_message_id(self, new_id: int):
        self.__text_message_id = new_id

    @property
    def town_keyboard_message_id(self) -> int:
        return self.__town_keyboard_message_id

    @town_keyboard_message_id.setter
    def town_keyboard_message_id(self, new_id: int):
        self.__town_keyboard_message_id = new_id

    @property
    def price_keyboard_message_id(self) -> int:
        return self.__price_keyboard_message_id

    @price_keyboard_message_id.setter
    def price_keyboard_message_id(self, new_id: int):
        self.__price_keyboard_message_id = new_id

    @property
    def min_price(self) -> int:
        return self.__min_price

    @min_price.setter
    def min_price(self, price: float):
        self.__min_price = price

    @property
    def max_price(self) -> int:
        return self.__max_price

    @max_price.setter
    def max_price(self, price: float):
        self.__max_price = price

    @property
    def distance_keyboard_message_id(self) -> int:
        return self.__distance_keyboard_message_id

    @distance_keyboard_message_id.setter
    def distance_keyboard_message_id(self, new_id: int):
        self.__distance_keyboard_message_id = new_id

    @property
    def image_choose_keyboard_message_id(self) -> int:
        return self.__image_choose_keyboard_message_id

    @image_choose_keyboard_message_id.setter
    def image_choose_keyboard_message_id(self, new_id: int):
        self.__image_choose_keyboard_message_id = new_id

    @property
    def image_cnt_choose_keyboard_message_id(self) -> int:
        return self.__image_cnt_choose_keyboard_message_id

    @image_cnt_choose_keyboard_message_id.setter
    def image_cnt_choose_keyboard_message_id(self, new_id: int):
        self.__image_cnt_choose_keyboard_message_id = new_id

    @property
    def date_in(self) -> date:
        return self.__date_in

    @date_in.setter
    def date_in(self, date_obj: date):
        self.__date_in = date_obj

    @property
    def date_out(self) -> date:
        return self.__date_out

    @date_out.setter
    def date_out(self, date_obj: date):
        self.__date_out = date_obj

    @property
    def hotels_data(self) -> LocalHotelsStorage:
        return self.__hotels_data

    @property
    def cur_global_page_ind(self) -> int:
        return self.__cur_global_page_ind

    @property
    def max_global_page_ind(self) -> int:
        return self.__max_global_page_ind

    @property
    def info_message_id(self) -> int:
        return self.__info_message_id

    @info_message_id.setter
    def info_message_id(self, new_id: int):
        self.__info_message_id = new_id

    @property
    def command_db_id(self):
        return self.__command_db_id

    @command_db_id.setter
    def command_db_id(self, new_id):
        self.__command_db_id = new_id

