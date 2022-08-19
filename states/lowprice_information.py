from telebot.handler_backends import State, StatesGroup


class UserLowPriceState(StatesGroup):
    city = State()
    hotels_number = State()
    image_choose = State()


class UserLowPriceData:
    def __init__(self):
        self.__city = ''
        self.__image_choose = False
        self.__cur_image_index = 1
        self.__max_image_index = 2
        self.__cur_page_index = 1
        self.__max_page_index = 5
        self.__photo_message_id = 0
        self.__text_message_id = 0

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def image_choose(self):
        return self.__image_choose

    @image_choose.setter
    def image_choose(self, image_choose):
        self.__image_choose = image_choose

    @property
    def max_image_index(self):
        return self.__max_image_index

    @property
    def cur_image_index(self):
        return self.__cur_image_index

    @cur_image_index.setter
    def cur_image_index(self, new_index):
        if (new_index > 0) and (new_index <= self.__max_image_index):
            self.__cur_image_index = new_index

    @property
    def cur_page_index(self):
        return self.__cur_page_index

    @cur_page_index.setter
    def cur_page_index(self, page_index):
        self.__cur_page_index = page_index

    @property
    def max_page_index(self):
        return self.__max_page_index

    @max_page_index.setter
    def max_page_index(self, page_cnt):
        self.__max_page_index = page_cnt

    @property
    def photo_message_id(self):
        return self.__photo_message_id

    @photo_message_id.setter
    def photo_message_id(self, new_id):
        self.__photo_message_id = new_id

    @property
    def text_message_id(self):
        return self.__text_message_id

    @text_message_id.setter
    def text_message_id(self, new_id):
        self.__text_message_id = new_id




