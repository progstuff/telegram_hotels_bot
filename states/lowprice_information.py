from telebot.handler_backends import State, StatesGroup


class UserLowPriceState(StatesGroup):
    city = State()
    hotels_number = State()
    image_choose = State()


class UserLowPriceData:
    def __init__(self):
        self.__city = ''
        self.__hotels_number = 0
        self.__image_choose = False

    @property
    def city(self):
        return self.__city

    @city.setter
    def city(self, city):
        self.__city = city

    @property
    def hotels_number(self):
        return self.__hotels_number

    @hotels_number.setter
    def hotels_number(self, hotels_number):
        self.__hotels_number = hotels_number

    @property
    def image_choose(self):
        return self.__image_choose

    @image_choose.setter
    def hotels_number(self, image_choose):
        self.__image_choose = image_choose


