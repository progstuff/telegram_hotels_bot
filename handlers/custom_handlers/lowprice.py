from loader import bot
from telebot.types import Message
from config_data.config import LOW_PRICE_COMMAND
from utils.misc.data_utils import get_complete_town_name
from states.lowprice_information import UserLowPriceState, UserLowPriceData
from keyboards.inline.hotels_chooser import get_hotels_numbers_choose_keyboard
from keyboards.inline.town_chooser import get_town_choose_keyboard

lowprice_data = dict()


@bot.message_handler(commands=[LOW_PRICE_COMMAND['command_name']])
def lowprice(message: Message) -> None:
    bot.set_state(message.from_user.id, UserLowPriceState.city, message.chat.id)
    bot.send_message(message.from_user.id, 'Вы выбрали показать топ бюджетных отелей в городе')
    bot.send_message(message.from_user.id, 'Шаг 1 из 3: Введите город')
    lowprice_data[message.chat.id] = UserLowPriceData()


@bot.message_handler(state=UserLowPriceState.city)
def lowprice_get_city(message: Message) -> None:
    towns_ru, towns_en = get_complete_town_name(message.text)
    if towns_ru is not None:
        if len(towns_ru) == 1:
            set_town(message, lowprice_data, towns_ru[0], towns_en[0])
        else:
            keyboard = get_town_choose_keyboard('town_lowprice', towns_ru, towns_en)
            mes = bot.send_message(message.from_user.id,
                             'Нет точного совпадения с имеющимися в базе городами, уточните город из предложенных. Если возможна ошибка ввода, введите город ещё раз',
                             reply_markup=keyboard)
            lowprice_data[message.chat.id].town_keyboard_message_id = mes.message_id

    else:
        bot.send_message(chat_id=message.chat.id, text='У меня в базе нет такого города, поиск выполнить не получится. Возможно ввод с ошибкой. Введите город ещё раз')
        bot.set_state(message.from_user.id, UserLowPriceState.city, message.chat.id)


def set_town(message, data_storage, town_ru, town_en):
    town = town_ru
    data_storage[message.chat.id].city_ru = town_ru
    data_storage[message.chat.id].city_en = town_en
    town_kbrd_message_id = data_storage[message.chat.id].town_keyboard_message_id
    if town_kbrd_message_id != 0:
        bot.delete_message(chat_id=message.chat.id, message_id=town_kbrd_message_id)
        bot.send_message(chat_id=message.chat.id,
                         text='Вы выбрали город: {0}'.format(town))
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Совпадение с одним городом в базе. Поиск будет выполнен для города: {0}'.format(town))

    bot.set_state(message.from_user.id, UserLowPriceState.hotels_number, message.chat.id)
    keyboard = get_hotels_numbers_choose_keyboard('lowprice_hotel_pages_number', [1, 5, 10, 15])
    bot.send_message(message.chat.id, 'Шаг 2 из 3: выберите сколько отелей показывать в выдаче',
                     reply_markup=keyboard)

#@bot.message_handler(state=UserLowPriceState.hotels_number)
#def lowprice_get_hotel_numbers(message: Message) -> None:
#    bot.send_message(message.from_user.id, 'tst')
#    #with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#    bot.send_message(message.from_user.id, lowprice_data[message.chat.id].city)
#    bot.delete_state(message.from_user.id, message.chat.id)


#@bot.message_handler(content_types='text')
#def lowprice_button_message(message: Message) -> None:
#    if message.text == LOW_PRICE_COMMAND['command_description']:
#        lowprice(message)