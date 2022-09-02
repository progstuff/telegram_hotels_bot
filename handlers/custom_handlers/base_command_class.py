from datetime import date

from telebot.types import CallbackQuery, Message, ReplyKeyboardRemove
from telegram_bot_calendar import LSTEP, DetailedTelegramCalendar

from config_data.config import (BEST_DEAL_COMMAND, HELP_COMMAND,
                                HIGH_PRICE_COMMAND, HISTORY_COMMAND,
                                LOW_PRICE_COMMAND, START_COMMAND)
from database.db_class_data import (CommandDataDb, CommandHotelsDb,
                                    HotelDb)
from database.command_local_data import CommandUserData
from keyboards.inline.hotels_chooser import get_hotels_numbers_choose_keyboard
from keyboards.inline.town_chooser import get_town_choose_keyboard
from keyboards.inline.yes_no import get_yes_no_keyboard
from keyboards.reply.show_menu import get_main_menu_keyboard
from loader import bot
from states.user_data_information import StatesGroup
from utils.misc.data_utils import get_complete_town_name, translate_date
from utils.misc.hotel_utils import change_hotel_page, hotel_image_slide_photo
from telebot.apihelper import ApiTelegramException
from loguru import logger

class BaseCommandHandlers:
    """
    класс, реализующий основной функционал для всех команд
    от него можно наследоваться и доопределять необходимое поведение для каждой команды
    например команда highprice от lowprice отличается только параметром по которому фильтруются
    отели при отправлении запроса на сервер, поэтому для реализации этой команды можно наследовать класс без изменений
    """
    def __init__(self, command_config: str, user_state_class: StatesGroup):
        self.__command_data = dict()
        self.__command_config = command_config
        self.__state_class = user_state_class
        self.__filter_value = 'PRICE'
        self.__cur_step = 1
        self.__max_steps_cnt = 5
        self.__hotels_pages = [1, 3, 5]
        self.__images_cnt = [1, 2, 3]
        self.calendar_id = "zero"

    def set_command_invoke_func(self, command_invoke_func):
        self.__command_invoke_func = command_invoke_func

    def clear_data(self, message: Message, is_need_reset):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_data = self.__command_data.get(chat_id, None)
        if is_need_reset:
            if user_data is not None:
                self.__command_data[chat_id].clear_data()
                bot.delete_state(user_id=user_id, chat_id=chat_id)
            self.__cur_step = 1
        self.__command_invoke_func(message)

    def set_max_steps_cnt(self, max_steps_cnt):
        self.__max_steps_cnt = max_steps_cnt

    def increase_step(self):
        if self.__cur_step < self.__max_steps_cnt:
            self.__cur_step += 1
        else:
            self.__cur_step = 1

    @property
    def state_class(self):
        return self.__state_class

    @property
    def command_data(self):
        return self.__command_data

    @property
    def command_config(self):
        return self.__command_config

    @property
    def max_steps_cnt(self):
        return self.__max_steps_cnt

    @property
    def cur_step(self):
        return self.__cur_step

    def set_filter_value(self, new_val: str) -> None:
        self.__filter_value = new_val

    def command_from_menu(self, message: Message) -> None:

        self.__cur_step = 1
        bot.send_message(message.chat.id, self.__command_config['command_welcome_mes'], reply_markup=ReplyKeyboardRemove())

        bot.set_state(message.from_user.id, self.__state_class.date_in, message.chat.id)
        self.__command_data[message.chat.id] = CommandUserData()
        self.choose_date(message.from_user.id, message.chat.id)

    def start_city_dialog(self, user_id: int, chat_id: int):
        bot.send_message(chat_id, 'Шаг {0} из {1}: Введите город'.format(self.cur_step, self.max_steps_cnt))
        bot.set_state(user_id, self.__state_class.city, chat_id)

    def choose_date(self, user_id: int, chat_id: int):
        if bot.get_state(user_id, chat_id) == self.__state_class.date_in.name:
            calendar, step = DetailedTelegramCalendar(min_date=date.today(), locale='ru', calendar_id=self.calendar_id).build()
            text = 'Шаг {0} из {1}: выберите дату заселения\nвыберите {2}'.format(self.cur_step,
                                                                            self.max_steps_cnt,
                                                                            translate_date(LSTEP[step]))
        else:
            calendar, step = DetailedTelegramCalendar(min_date=date.today(), locale='ru', calendar_id=self.calendar_id).build()
            text = 'Шаг {0} из {1}: выберите дату выселения\nвыберите {2}'.format(self.cur_step,
                                                                                   self.max_steps_cnt,
                                                                                   translate_date(LSTEP[step]))
        bot.send_message(chat_id,
                         text,
                         reply_markup=calendar)

    def set_calendar_callback(self):
        @bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=self.calendar_id))
        def get_date(call: CallbackQuery):

            if bot.get_state(call.from_user.id, call.message.chat.id) == self.__state_class.date_in.name:
                result, key, step = DetailedTelegramCalendar(min_date=date.today(), locale='ru', calendar_id=self.calendar_id).process(call.data)
                text = 'Шаг {0} из {1}: выберите дату заселения\n выберите {2}'.format(self.cur_step,
                                                                                       self.max_steps_cnt,
                                                                                       translate_date(LSTEP[step]))
            else:
                date_in = self.command_data[call.message.chat.id].date_in
                result, key, step = DetailedTelegramCalendar(min_date=date_in, locale='ru', calendar_id=self.calendar_id).process(call.data)
                text = 'Шаг {0} из {1}: выберите дату выселения\n выберите {2}'.format(self.cur_step,
                                                                                       self.max_steps_cnt,
                                                                                       translate_date(LSTEP[step]))

            if not result and key:
                bot.edit_message_text(text,
                                      call.message.chat.id,
                                      call.message.message_id,
                                      reply_markup=key)
            elif result:
                if bot.get_state(call.from_user.id, call.message.chat.id) == self.__state_class.date_in.name:
                    bot.edit_message_text('Шаг {0} из {1}: Вы выбрали дату заселения {2}'.format(self.cur_step,
                                                                                                 self.max_steps_cnt,
                                                                                                 result.strftime('%d-%m-%Y')),
                                          call.message.chat.id,
                                          call.message.message_id)
                    bot.set_state(call.from_user.id, self.__state_class.date_out, call.message.chat.id)
                    self.command_data[call.message.chat.id].date_in = result
                    self.increase_step()
                    self.choose_date(call.from_user.id, call.message.chat.id)
                else:
                    bot.edit_message_text('Шаг {0} из {1}: Вы выбрали дату выселения {2}'.format(self.cur_step,
                                                                                                 self.max_steps_cnt,
                                                                                                 result.strftime('%d-%m-%Y')),
                                          call.message.chat.id,
                                          call.message.message_id)
                    self.command_data[call.message.chat.id].date_out = result
                    self.increase_step()
                    self.start_city_dialog(call.from_user.id, call.message.chat.id)

    def set_get_city_handler(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class

        @bot.message_handler(state=CUR_STATE.city)
        def get_city(message: Message) -> None:
            is_command, is_need_reset = self.is_command_message(message)
            if not is_command:
                towns_ru, towns_en = get_complete_town_name(message.text)
                if towns_ru is not None:
                    if len(towns_ru) == 1:
                        self.set_town(message, self.__command_data, towns_ru[0], towns_en[0])
                        self.step_after_town_choose(message.from_user.id, message.chat.id)
                    else:
                        keyboard = get_town_choose_keyboard(CUR_COMMAND['town_choose_kbrd_key'], towns_ru, towns_en)
                        town_kbrd_message_id = self.command_data[message.chat.id].town_keyboard_message_id
                        if town_kbrd_message_id != 0:
                            bot.delete_message(chat_id=message.chat.id, message_id=town_kbrd_message_id)

                        mes = bot.send_message(message.from_user.id,
                                         'Нет точного совпадения с имеющимися в базе городами, уточните город из предложенных. '
                                         'Если возможна ошибка ввода, введите город ещё раз',
                                         reply_markup=keyboard)
                        self.__command_data[message.chat.id].town_keyboard_message_id = mes.message_id

                else:
                    bot.send_message(chat_id=message.chat.id, text='У меня в базе нет такого города, поиск выполнить не получится. '
                                                                   'Возможно ввод с ошибкой. Введите город ещё раз')
                    bot.set_state(message.from_user.id, CUR_STATE.city, message.chat.id)
            else:
                self.clear_data(message, is_need_reset)

    def set_hotels__cnt_choose_page_handler(self):
        CUR_STATE = self.__state_class

        @bot.message_handler(state=CUR_STATE.hotels_number)
        def get_hotels_cnt_choose_page(message: Message) -> None:
            is_command, is_need_reset = self.is_command_message(message)
            if not is_command:
                bot.delete_message(chat_id=message.chat.id,
                                   message_id=self.__command_data[message.chat.id].__pages_cnt_keyboard_message_id)
                keyboard = get_hotels_numbers_choose_keyboard(self.__command_config['hotels_pages_number_key'],
                                                              self.__hotels_pages)
                mes = bot.send_message(message.chat.id,
                                 'Пожалуйста, выберите из предложенных вариантов. \n'
                                 'Шаг {0} из {1}: выберите сколько отелей показывать в выдаче'.format(self.cur_step,
                                                                                                      self.max_steps_cnt),
                                 reply_markup=keyboard)
                self.__command_data[message.chat.id].__pages_cnt_keyboard_message_id = mes.message_id
            else:
                self.clear_data(message, is_need_reset)

    def set_image_choose_handler(self):
        CUR_STATE = self.__state_class
        CUR_COMMAND = self.__command_config

        @bot.message_handler(state=CUR_STATE.image_choose)
        def get_image_choose(message: Message) -> None:
            is_command, is_need_reset = self.is_command_message(message)
            if not is_command:
                keyboard = get_yes_no_keyboard(CUR_COMMAND['image_dialog_key'])

                bot.delete_message(chat_id=message.chat.id,
                                   message_id=self.__command_data[message.chat.id].image_choose_keyboard_message_id)
                mes = bot.send_message(chat_id=message.chat.id,
                                       text='Выберите, пожалуйста, из предложенных вариантов. \n'
                                            'Шаг {0} из {1}: загружать фото отелей?'.format(self.cur_step,
                                                                                            self.max_steps_cnt),
                                       reply_markup=keyboard)
                self.__command_data[message.chat.id].image_choose_keyboard_message_id = mes.message_id
            else:
                self.clear_data(message, is_need_reset)

    def set_image_cnt_choose_handler(self):
        CUR_STATE = self.__state_class
        CUR_COMMAND = self.__command_config

        @bot.message_handler(state=CUR_STATE.max_images_cnt)
        def get_image_cnt_choose(message: Message) -> None:
            is_command, is_need_reset = self.is_command_message(message)
            if not is_command:
                bot.delete_message(chat_id=message.chat.id,
                                   message_id=self.__command_data[message.chat.id].image_cnt_choose_keyboard_message_id)
                keyboard = get_hotels_numbers_choose_keyboard(CUR_COMMAND['image_pages_number_key'],
                                                              self.__images_cnt)
                mes = bot.send_message(chat_id=message.chat.id,
                                       text='Пожалуйста, выберите из предложенных вариантов.\n'
                                            'Шаг {0} из {1}: выберите сколько фото показывать для каждого отеля'
                                       .format(self.cur_step, self.max_steps_cnt),
                                       reply_markup=keyboard)
                self.__command_data[message.chat.id].image_cnt_choose_keyboard_message_id = mes.message_id
            else:
                self.clear_data(message, is_need_reset)

    def set_data_received_handler(self):
        CUR_STATE = self.__state_class

        @bot.message_handler(state=CUR_STATE.data_received)
        def data_receieved_handler(message: Message) -> None:
            is_command, is_need_reset = self.is_command_message(message)
            if not is_command:
                pass
            else:
                self.clear_data(message, is_need_reset)

    def set_hotels_page_callback(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['hotels_pages_number_key'])
        def hotels_page_callback(call: CallbackQuery) -> None:

            pages_cnt = int(call.data.split('#')[1])
            self.__command_data[call.message.chat.id].max_page_index = pages_cnt
            keyboard = get_yes_no_keyboard(CUR_COMMAND['image_dialog_key'])

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Шаг {0} из {1}: вы выбрали максимальное количество отелей показа за раз: {2}'
                                  .format(self.cur_step, self.max_steps_cnt, pages_cnt))

            self.increase_step()  # был шаг 2
            mes = bot.send_message(chat_id=call.message.chat.id,
                             text='Шаг {0} из {1}: загружать фото отелей?'.format(self.cur_step, self.max_steps_cnt),
                             reply_markup=keyboard)
            self.__command_data[call.message.chat.id].image_choose_keyboard_message_id = mes.message_id
            bot.set_state(call.from_user.id, CUR_STATE.image_choose, call.message.chat.id)

    def set_hotels_show_image_choose_callback(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['image_dialog_key'])
        def hotels_show_image_choose(call: CallbackQuery) -> None:
            if call.data.split('#')[1] == 'yes':
                self.__command_data[call.message.chat.id].image_choose = True

                keyboard = get_hotels_numbers_choose_keyboard(CUR_COMMAND['image_pages_number_key'], self.__images_cnt)
                bot.delete_message(chat_id=call.message.chat.id, message_id=self.__command_data[call.message.chat.id].image_choose_keyboard_message_id)
                mes = bot.send_message(chat_id=call.message.chat.id,
                                       text='Шаг {0} из {1}: выберите сколько фото показывать для каждого отеля'
                                       .format(self.cur_step, self.max_steps_cnt),
                                       reply_markup=keyboard)
                self.__command_data[call.message.chat.id].image_cnt_choose_keyboard_message_id = mes.message_id
                bot.set_state(call.from_user.id, CUR_STATE.max_images_cnt, call.message.chat.id)
            else:
                bot.delete_message(chat_id=call.message.chat.id,
                                   message_id=self.__command_data[call.message.chat.id].image_choose_keyboard_message_id)
                self.__command_data[call.message.chat.id].image_choose = False
                bot.send_message(chat_id=call.message.chat.id,
                                 text='Шаг {0} из {1}: Вы выбрали не показывать фото отелей'
                                 .format(self.cur_step, self.max_steps_cnt))
                bot.set_state(call.from_user.id, CUR_STATE.data_received, call.message.chat.id)

                self.__command_data[call.message.chat.id].reset_global_page_ind()
                self.load_data_from_server(call.from_user.id,
                                           call.message.chat.id,
                                           self.__command_data,
                                           True)
                main_menu_keyboard = get_main_menu_keyboard()
                bot.send_message(call.message.chat.id, "Какие отели ещё показать?", reply_markup=main_menu_keyboard)


    def set_hotels_show_image_cnt_callback(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['image_pages_number_key'])
        def hotels_show_image_cnt(call: CallbackQuery) -> None:
            max_images_cnt = int(call.data.split('#')[1])
            self.__command_data[call.message.chat.id].max_image_index = max_images_cnt

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Шаг {0} из {1}: Вы выбрали показывать по {2} фото для отеля'
                                  .format(self.cur_step, self.max_steps_cnt, max_images_cnt))
            self.increase_step()  # был шаг 3

            bot.set_state(call.from_user.id, CUR_STATE.data_received, call.message.chat.id)
            self.__command_data[call.message.chat.id].reset_global_page_ind()
            self.load_data_from_server(call.from_user.id, call.message.chat.id,  self.__command_data, True)
            main_menu_keyboard = get_main_menu_keyboard()
            bot.send_message(call.message.chat.id, "Какие отели ещё показать?", reply_markup=main_menu_keyboard)

    def set_hotel_page_callback(self) -> None:
        CUR_COMMAND = self.__command_config

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['hotels_kbrd_page_key'])
        def hotel_page_callback(call: CallbackQuery) -> None:
            data = call.data.split('#')[1]
            if data == "backward":
                self.__command_data[call.message.chat.id].decrease_global_page_ind()
                page_ind = self.__command_data[call.message.chat.id].max_page_index
                self.load_data_from_db(call.message.chat.id, self.__command_data)
            elif data == "forward_web":
                self.__command_data[call.message.chat.id].increase_global_page_ind()
                self.load_data_from_server(call.from_user.id, call.message.chat.id, self.__command_data, False)
                page_ind = 1
            elif data == "forward":
                self.__command_data[call.message.chat.id].increase_global_page_ind()
                page_ind = 1
                self.load_data_from_db(call.message.chat.id, self.__command_data)
            else:
                page_ind = int(data)

            image_ind = 1
            change_hotel_page(call.message.chat.id,
                              page_ind, image_ind,
                              False,
                              self.__command_data,
                              CUR_COMMAND['hotels_kbrd_page_key'],
                              CUR_COMMAND['image_kbrd_page_key'])

    def set_hotel_image_callback(self) -> None:
        CUR_COMMAND = self.__command_config

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['image_kbrd_page_key'])
        def hotel_image_callback(call: CallbackQuery) -> None:
            hotel_image_slide_photo(call,
                                    self.__command_data,
                                    CUR_COMMAND['hotels_kbrd_page_key'],
                                    CUR_COMMAND['image_kbrd_page_key'])

    def set_town_callback(self) -> None:
        CUR_COMMAND = self.__command_config

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['town_choose_kbrd_key'])
        def town_callback(call: CallbackQuery) -> None:
            town_en = call.data.split('#')[1]
            towns_ru, towns_en = get_complete_town_name(town_en)
            self.set_town(call.message, self.__command_data, towns_ru[0], town_en)
            self.step_after_town_choose(call.from_user.id, call.message.chat.id)

    def get_info_message(self, data_storage: dict, chat_id: int) -> str:
        pages_cnt = data_storage[chat_id].max_page_index
        city = data_storage[chat_id].city_ru
        mes = "Все данные получены. Выбраны следующие параметры запроса:\n\n"
        mes += "  дата заселения: {}\n".format(data_storage[chat_id].date_in.strftime("%d-%m-%Y"))
        mes += "  дата выселения: {}\n".format(data_storage[chat_id].date_out.strftime("%d-%m-%Y"))
        mes += "  город: {}\n".format(city)
        mes += "  количество отелей в выдаче: {}\n".format(pages_cnt)
        if data_storage[chat_id].image_choose:
            max_images_cnt = data_storage[chat_id].max_image_index
            mes += "  количество фото для отеля: {0}\n\n".format(max_images_cnt)
        else:
            mes += "  не показывать фото отелей\n\n"
        mes += "Начинаю загрузку отелей"

        return mes

    def set_town(self, message: Message, data_storage: dict, town_ru: str, town_en: str) -> None:
        town = town_ru
        data_storage[message.chat.id].city_ru = town_ru
        data_storage[message.chat.id].city_en = town_en
        town_kbrd_message_id = data_storage[message.chat.id].town_keyboard_message_id
        if town_kbrd_message_id != 0:
            bot.delete_message(chat_id=message.chat.id, message_id=town_kbrd_message_id)
            bot.send_message(chat_id=message.chat.id,
                             text='Шаг {0} из {1}: Вы выбрали город: {2}'
                             .format(self.cur_step, self.max_steps_cnt, town))
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Шаг {0} из {1}: Совпадение с одним городом в базе.\nПоиск будет выполнен для города: {2}'
                             .format(self.cur_step, self.max_steps_cnt, town))
        self.increase_step() # был шаг 1

    def step_after_town_choose(self, user_id: int, chat_id: int):
        bot.set_state(user_id, self.__state_class.hotels_number, chat_id)
        self.hotels_cnt_choose_step(chat_id)

    def hotels_cnt_choose_step(self, chat_id: int):
        keyboard = get_hotels_numbers_choose_keyboard(self.__command_config['hotels_pages_number_key'],
                                                      self.__hotels_pages)
        mes = bot.send_message(chat_id,
                               'Шаг {0} из {1}: выберите сколько отелей показывать в выдаче'
                               .format(self.cur_step, self.max_steps_cnt),
                               reply_markup=keyboard)
        self.__command_data[chat_id].__pages_cnt_keyboard_message_id = mes.id

    def try_to_delete_hotel_page_message(self, chat_id: int, data_storage: dict):
        try:
            bot.delete_message(chat_id=chat_id,
                               message_id=data_storage[chat_id].info_message_id)
        except ApiTelegramException:
            logger.warning('чат {}: не удалось найти/удалить информационное сообщение'.format(chat_id))
        try:
            bot.delete_message(chat_id=chat_id,
                               message_id=data_storage[chat_id].photo_message_id)
        except ApiTelegramException:
            logger.warning('чат {}: не удалось найти/удалить сообщение с фото отеля'.format(chat_id))

        try:
            bot.delete_message(chat_id=chat_id,
                               message_id=data_storage[chat_id].text_message_id)
        except ApiTelegramException:
            logger.warning('чат {}: не удалось найти/удалить сообщение с описанием отеля'.format(chat_id))

    def load_data_from_db(self, chat_id: int, data_storage: dict) -> None:
        #self.show_info_message(chat_id, data_storage)
        local_hotels_storage = data_storage[chat_id].hotels_data
        hotels_cnt = local_hotels_storage.get_hotel_data_from_db(command_id=data_storage[chat_id].command_db_id,
                                                                 page_ind=data_storage[chat_id].cur_global_page_ind,
                                                                 page_size=data_storage[chat_id].max_page_index)
        self.show_data(hotels_cnt, chat_id, data_storage, False)

    def load_data_from_server(self, user_id: int, chat_id: int, data_storage: dict, is_first: bool) -> None:
        self.show_info_message(chat_id, data_storage)
        local_hotels_storage = data_storage[chat_id].hotels_data

        hotels_cnt = local_hotels_storage.get_hotel_data_from_server(data_storage[chat_id].city_en,
                                                                     data_storage[chat_id].date_in,
                                                                     data_storage[chat_id].date_out,
                                                                     data_storage[chat_id].max_page_index,
                                                                     data_storage[chat_id].cur_global_page_ind,
                                                                     self.__filter_value,
                                                                     data_storage[chat_id].min_price,
                                                                     data_storage[chat_id].max_price)
        if hotels_cnt > 0:
            if is_first:
                data_storage[chat_id].command_db_id = self.add_command_data_to_db(user_id, chat_id, data_storage)
            else:
                self.append_hotels_data_to_db(chat_id, data_storage)

        self.show_data(hotels_cnt, chat_id, data_storage, True)

    def show_info_message(self, chat_id: int, data_storage: dict):
        self.try_to_delete_hotel_page_message(chat_id, data_storage)
        text = self.get_info_message(data_storage, chat_id)
        mes = bot.send_message(chat_id=chat_id, text=text)
        data_storage[chat_id].info_message_id = mes.message_id

    def show_data(self, hotels_cnt: int, chat_id: int, data_storage: dict, is_need_recreate: bool) -> None:
        local_hotels_storage = data_storage[chat_id].hotels_data
        #####################
        text = self.get_info_message(data_storage, chat_id)
        if hotels_cnt > 0:
            if hotels_cnt < data_storage[chat_id].max_page_index:
                data_storage[chat_id].max_page_index = hotels_cnt
            text = text + "\nДоступно отелей для просмотра: {}".format(hotels_cnt)

            try:
                bot.edit_message_text(chat_id=chat_id, text=text, message_id=data_storage[chat_id].info_message_id)
            except ApiTelegramException:
                logger.warning("чат - {}: повтор описания параметров запроса (без фото)".format(chat_id))

            image_choose = data_storage[chat_id].image_choose
            if image_choose:
                max_images_cnt = data_storage[chat_id].max_image_index
                for hotel_ind in range(1, hotels_cnt + 1):
                    images_cnt = local_hotels_storage.get_images_links_from_server(hotel_ind,
                                                                                   max_images_cnt)
                    text = text + "\nполучено изображений для отеля №{0}: {1}".format(hotel_ind, images_cnt)

                    try:
                        bot.edit_message_text(chat_id=chat_id, text=text, message_id=data_storage[chat_id].info_message_id)
                    except ApiTelegramException:
                        logger.warning("чат - {}: повтор описания параметров запроса (с фото)".format(chat_id))

            page_ind = 1
            image_ind = 1
            change_hotel_page(chat_id,
                              page_ind,
                              image_ind,
                              is_need_recreate,
                              data_storage,
                              self.__command_config['hotels_kbrd_page_key'],
                              self.__command_config['image_kbrd_page_key'])
        else:
            text = text + '\nНет отелей для просмотра'
            bot.edit_message_text(chat_id=chat_id, text=text, message_id=data_storage[chat_id].info_message_id)

    def is_command_message(self, message):
        if (message.text == LOW_PRICE_COMMAND['command_description'] or
            message.text == ('/' + LOW_PRICE_COMMAND['command_name'])):
            return True, True
        if (message.text == HIGH_PRICE_COMMAND['command_description'] or
            message.text == ('/' + HIGH_PRICE_COMMAND['command_name'])):
            return True, True
        if (message.text == BEST_DEAL_COMMAND['command_description'] or
            message.text == ('/' + BEST_DEAL_COMMAND['command_name'])):
            return True, True
        if message.text == ('/' + START_COMMAND['command_name']):
            return True, True
        if message.text == ('/' + HELP_COMMAND['command_name']):
            return True, False
        if (message.text == HISTORY_COMMAND['command_description'] or
            message.text == ('/' + HISTORY_COMMAND['command_name'])):
            return True, False
        return False, False

    def add_command_data_to_db(self, user_id, chat_id, data_storage) -> int:
        com_data = CommandDataDb.create(user_id=user_id,
                                        command_name=self.__command_config['command_name'],
                                        invoke_time=date.today(),
                                        date_in=data_storage[chat_id].date_in,
                                        date_out=data_storage[chat_id].date_out,
                                        town_ru=data_storage[chat_id].city_ru,
                                        town_en=data_storage[chat_id].city_en)

        local_hotels_storage = data_storage[chat_id].hotels_data
        hotels_cnt = local_hotels_storage.get_hotels_cnt()
        for hotel_ind in range(1, hotels_cnt + 1):
            hotel = local_hotels_storage.get_hotel(hotel_ind)
            hotel_db = HotelDb.insert(
                hotel_id=hotel.id,
                name=hotel.name,
                address=hotel.address,
                distance_to_center=hotel.center_dist,
                one_day_price=hotel.exact_current,
                days_cnt=hotel.days_cnt,
                total_price=hotel.total_cost,
                url=hotel.hotel_link
            ).on_conflict('replace').execute()
            CommandHotelsDb.create(command_data=com_data,
                                   hotel_id=hotel_db)
        return com_data.id

    def append_hotels_data_to_db(self, chat_id, data_storage) -> int:
        com_id = data_storage[chat_id].command_db_id
        local_hotels_storage = data_storage[chat_id].hotels_data
        hotels_cnt = local_hotels_storage.get_hotels_cnt()
        for hotel_ind in range(1, hotels_cnt + 1):
            hotel = local_hotels_storage.get_hotel(hotel_ind)
            hotel_db = HotelDb.insert(
                hotel_id=hotel.id,
                name=hotel.name,
                address=hotel.address,
                distance_to_center=hotel.center_dist,
                one_day_price=hotel.exact_current,
                days_cnt=hotel.days_cnt,
                total_price=hotel.total_cost,
                url=hotel.hotel_link
            ).on_conflict('replace').execute()
            CommandHotelsDb.create(command_data=com_id,
                                   hotel_id=hotel_db)

    def set_handlers(self) -> None:
        self.set_get_city_handler()
        self.set_hotels__cnt_choose_page_handler()
        self.set_image_choose_handler()
        self.set_image_cnt_choose_handler()
        self.set_data_received_handler()

    def set_callbacks(self) -> None:
        self.set_calendar_callback()
        self.set_town_callback()
        self.set_hotels_page_callback()
        self.set_hotels_show_image_choose_callback()
        self.set_hotels_show_image_cnt_callback()
        self.set_hotel_page_callback()
        self.set_hotel_image_callback()

