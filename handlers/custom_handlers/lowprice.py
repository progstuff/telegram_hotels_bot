from loader import bot
from telebot.types import Message
from config_data.config import LOW_PRICE_COMMAND
from utils.misc.rapid_api_utils import get_lowprice_hotels
from utils.misc.data_utils import get_complete_town_name
from states.lowprice_information import UserLowPriceState
from utils.misc.hotels_parser import Hotel
from keyboards.inline.hotels_chooser import get_hotels_numbers_choose_keyboard
from config_data.config import HOTEL_PAGES
import json

from telegram_bot_pagination import InlineKeyboardPaginator


@bot.message_handler(commands=[LOW_PRICE_COMMAND['command_name']])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserLowPriceState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'вы выбрали показать топ самых дешевых отелей в городе. Введите город')


@bot.message_handler(state=UserLowPriceState.city)
def lowprice_get_city(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        town = get_complete_town_name(message.text)
        if town is not None:
            data['city'] = town
            bot.send_message(message.from_user.id, 'Поиск в городе: {0}'.format(town), )
            bot.set_state(message.from_user.id, UserLowPriceState.hotels_number, message.chat.id)

            keyboard = get_hotels_numbers_choose_keyboard()
            bot.send_message(message.from_user.id, 'выберите по сколько отелей показывать', reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, 'У меня в базе нет такого города. Возможно ввод с ошибкой. Введите город ещё раз:')
            bot.set_state(message.from_user.id, UserLowPriceState.city, message.chat.id)


#@bot.message_handler(state=UserLowPriceState.hotels_number)
#def lowprice_get_hotel_numbers(message: Message) -> None:
#    bot.send_message(message.from_user.id, 'Все данные получены, начинаю загрузку отелей')
#    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(content_types='text')
def lowprice_button_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description']:
        lowprice(message)