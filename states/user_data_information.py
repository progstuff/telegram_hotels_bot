from datetime import date, timedelta
from telebot.handler_backends import State, StatesGroup


class UserLowPriceState(StatesGroup):
    date_in = State()
    date_out = State()
    city = State()
    hotels_number = State()
    image_choose = State()
    max_images_cnt = State()
    data_received = State()


class UserHighPriceState(StatesGroup):
    date_in = State()
    date_out = State()
    city = State()
    hotels_number = State()
    image_choose = State()
    max_images_cnt = State()
    data_received = State()



class UserBestDealState(StatesGroup):
    date_in = State()
    date_out = State()
    city = State()
    hotels_number = State()
    hotels_price = State()
    image_choose = State()
    max_images_cnt = State()
    distance_to_center = State()
    undefined_state = State()
    data_received = State()









