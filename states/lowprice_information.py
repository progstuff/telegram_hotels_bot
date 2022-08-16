from telebot.handler_backends import State, StatesGroup


class UserLowPriceState(StatesGroup):
    city = State()
    hotels_number = State()
