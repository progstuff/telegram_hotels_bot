from telebot.types import Message

from loader import bot
from database.command_history_data import CommandDataDb, CommandHotelsDb, HotelDb
from keyboards.inline.hotels_chooser import history_hotels_paginator
from config_data.config import HISTORY_COMMAND
from telebot.types import CallbackQuery


history_data = dict()


def bot_history(message: Message) -> None:
    user_id = message.from_user.id
    command_rows = CommandDataDb.select().where(CommandDataDb.user_id == user_id)
    i = 1
    history_data[message.chat.id] = list()

    for row in reversed(command_rows):

        com_mes = row.get_str_view() + '\n'
        hotels = HotelDb.select().join(CommandHotelsDb).where(CommandHotelsDb.command_data == row)
        for hotel in reversed(hotels):
            mes = '\n'.join([com_mes, hotel.get_str_view()])
            history_data[message.chat.id].append(mes)
            i += 1
            if i > 5:
                break
        if i > 5:
            break

    if len(history_data[message.chat.id]) > 0:
        hotels_keyboard = history_hotels_paginator(1, len(history_data[message.chat.id]), HISTORY_COMMAND['hotels_pages_number_key'])
        bot.send_message(chat_id=message.chat.id,
                         text=history_data[message.chat.id][0],
                         reply_markup=hotels_keyboard.markup)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text='Записей с отелями не найдено')


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == HISTORY_COMMAND['hotels_pages_number_key'])
def update_history_hotel_message(call: CallbackQuery) -> None:
    page_index = int(call.data.split('#')[1])
    hotels_keyboard = history_hotels_paginator(page_index, len(history_data[call.message.chat.id]),
                                               HISTORY_COMMAND['hotels_pages_number_key'])
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          text=history_data[call.message.chat.id][page_index-1],
                          reply_markup=hotels_keyboard.markup)





