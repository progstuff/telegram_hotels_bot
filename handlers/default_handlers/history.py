from math import ceil

from telebot.types import CallbackQuery, Message
from telebot.apihelper import ApiTelegramException
from config_data.config import HISTORY_COMMAND
from database.db_class_data import (CommandDataDb, CommandHotelsDb,
                                    HotelDb)
from keyboards.inline.hotels_chooser import history_hotels_paginator
from loader import bot
from loguru import logger

class HistoryCommand:

    def __init__(self):
        self.__history_data = dict()
        self.page_size = 5

    def load_page(self, chat_id: int, page: int) -> None:
        self.__history_data[chat_id]['cur_page_ind'] = page
        cur_page = self.__history_data[chat_id]['max_pages'] - page + 1

        start_ind = (cur_page - 1) * self.page_size
        end_ind = start_ind + self.page_size
        n = len(self.__history_data[chat_id]['all_hotels'])
        if end_ind > n:
            end_ind = n
        self.__history_data[chat_id]['cur_page_hotels'] = list()
        for ind in range(start_ind, end_ind):
            self.__history_data[chat_id]['cur_page_hotels'].insert(
                0,
                self.__history_data[chat_id]['all_hotels'][ind])

    def increase_global_page_ind(self, chat_id: int) -> None:
        cur_page_ind = self.__history_data[chat_id]['cur_page_ind']
        max_page_ind = self.__history_data[chat_id]['max_pages']
        if cur_page_ind < max_page_ind:
            cur_page_ind += 1
            self.__history_data[chat_id]['cur_page_ind'] = cur_page_ind

    def decrease_global_page_ind(self, chat_id: int) -> None:
        cur_page_ind = self.__history_data[chat_id]['cur_page_ind']
        if cur_page_ind > 1:
            cur_page_ind -= 1
            self.__history_data[chat_id]['cur_page_ind'] = cur_page_ind

    def show_user_history(self, message: Message) -> None:
        bot.send_message(chat_id=message.chat.id,
                         text=HISTORY_COMMAND["command_welcome_mes"])
        user_id = message.from_user.id
        command_rows = CommandDataDb.select().where(CommandDataDb.user_id == user_id)
        self.__history_data[message.chat.id] = dict()
        self.__history_data[message.chat.id]['all_hotels'] = list()

        for row in reversed(command_rows):
            com_mes = row.get_str_view() + '\n'
            hotels = HotelDb.select().join(CommandHotelsDb).where(CommandHotelsDb.command_data == row)
            for hotel in reversed(hotels):
                hotel.update_total_price(row.date_in, row.date_out)
                mes = '\n'.join([com_mes, hotel.get_str_view()])
                self.__history_data[message.chat.id]['all_hotels'].append(mes)
            self.__history_data[message.chat.id]['max_pages'] = ceil(len(self.__history_data[message.chat.id]['all_hotels'])/self.page_size)
            self.__history_data[message.chat.id]['cur_page_ind'] = self.__history_data[message.chat.id]['max_pages']

        if len(self.__history_data[message.chat.id]['all_hotels']) > 0:
            self.load_page(message.chat.id, self.__history_data[message.chat.id]['max_pages'])
            hotels_keyboard = history_hotels_paginator(len(self.__history_data[message.chat.id]['cur_page_hotels']),
                                                       len(self.__history_data[message.chat.id]['cur_page_hotels']),
                                                       self.__history_data[message.chat.id]['cur_page_ind'],
                                                       self.__history_data[message.chat.id]['max_pages'],
                                                       HISTORY_COMMAND['hotels_pages_number_key'])
            bot.send_message(chat_id=message.chat.id,
                             text=self.__history_data[message.chat.id]['cur_page_hotels'][-1],
                             reply_markup=hotels_keyboard.markup,
                             disable_web_page_preview=True)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Записей с отелями не найдено')

    def set_callbacks(self) -> None:
        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == HISTORY_COMMAND['hotels_pages_number_key'])
        def update_history_hotel_message(call: CallbackQuery) -> None:
            data = call.data.split('#')[1]
            if data == 'forward':
                self.increase_global_page_ind(call.message.chat.id)
                global_page_index = self.__history_data[call.message.chat.id]['cur_page_ind']
                self.load_page(call.message.chat.id, global_page_index)
                page_index = len(self.__history_data[call.message.chat.id]['cur_page_hotels'])
            elif data == 'backward':
                self.decrease_global_page_ind(call.message.chat.id)
                global_page_index = self.__history_data[call.message.chat.id]['cur_page_ind']
                self.load_page(call.message.chat.id, global_page_index)
                page_index = len(self.__history_data[call.message.chat.id]['cur_page_hotels'])
            else:
                page_index = int(data)

            try:
                hotels_keyboard = history_hotels_paginator(page_index,
                                                           len(self.__history_data[call.message.chat.id]['cur_page_hotels']),
                                                           self.__history_data[call.message.chat.id]['cur_page_ind'],
                                                           self.__history_data[call.message.chat.id]['max_pages'],
                                                           HISTORY_COMMAND['hotels_pages_number_key'])
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.id,
                                      text=self.__history_data[call.message.chat.id]['cur_page_hotels'][page_index-1],
                                      reply_markup=hotels_keyboard.markup,
                                      disable_web_page_preview=True)
            except ApiTelegramException:
                logger.warning("чат - {}: переключение отеля в истории - текст без изменений".format(call.message.chat.id))


history_handlers = HistoryCommand()
history_handlers.set_callbacks()






