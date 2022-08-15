from loader import bot
from telebot.types import Message
from config_data.config import LOW_PRICE_COMMAND
from utils.misc.rapid_api_utils import get_lowprice_hotels
from utils.misc.data_utils import get_complete_town_name
from states.lowprice_information import UserLowPriceState
import json


@bot.message_handler(commands=[LOW_PRICE_COMMAND['command_name']])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserLowPriceState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'вы выбрали показать топ самых дешевых отелей в городе. Введите город')


@bot.message_handler(state=UserLowPriceState.city)
def lowprice_get_city(message: Message) -> None:

    #bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        town = get_complete_town_name(message.text)
        if town is not None:
            data['city'] = town
            bot.send_message(message.from_user.id, 'Поиск в городе: {0}'.format(town), )
            print(len(town))
        else:
            bot.send_message(message.from_user.id, 'У меня в базе нет такого города. Возможно ввод с ошибкой. Введите город ещё раз:')
            bot.set_state(message.from_user.id, UserLowPriceState.city, message.chat.id)

            #is_success, hotels = get_lowprice_hotels('new york')
    #if is_success:
    #   with open('result.json', 'w') as file:
    #       json.dump(hotels, file, indent=4)
    #print(hotels)


@bot.message_handler(content_types='text')
def lowprice_button_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description']:
        lowprice(message)