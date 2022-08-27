from telebot.handler_backends import State, StatesGroup


class UserData:

    def __init__(self):
        self.__city_en = ''
        self.__city_ru = ''
        self.__min_price = -1
        self.__max_price = -1
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

    def clear_data(self):
        self.__city_en = ''
        self.__city_ru = ''
        self.__min_price = -1
        self.__max_price = -1
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


class UserLowPriceState(StatesGroup):
    city = State()
    hotels_number = State()
    image_choose = State()
    max_images_cnt = State()
    data_received = State


class UserHighPriceState(StatesGroup):
    city = State()
    hotels_number = State()
    image_choose = State()
    max_images_cnt = State()
    data_received = State


class UserBestDealState(StatesGroup):
    city = State()
    hotels_number = State()
    hotels_price = State()
    image_choose = State()
    max_images_cnt = State()
    distance_to_center = State()
    undefined_state = State()
    data_received = State








