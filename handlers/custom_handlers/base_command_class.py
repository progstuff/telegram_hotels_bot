from loader import bot
from telebot.types import Message

from utils.misc.data_utils import get_complete_town_name

from keyboards.inline.hotels_chooser import get_hotels_numbers_choose_keyboard
from keyboards.inline.town_chooser import get_town_choose_keyboard

from keyboards.inline.yes_no import get_yes_no_keyboard
from utils.misc.hotel_utils import change_hotel_page, hotel_image_slide_photo
from db.hotels_parser import get_hotel_data_from_server, get_images_links_from_server, get_hotel
from telebot.types import CallbackQuery
from states.user_data_information import UserData, StatesGroup
from telebot.handler_backends import State

class BaseCommandHandlers:
    """
    класс, реализующий основной функционал для всех команд
    от него можно наследоваться и доопределять необходимое поведение для каждой команды
    например команда highprice от lowprice отличается только параметром по которому фильтруются
    отели при отправлении запроса на сервер, поэтому для реализации этой команды можно наследовать класс без изменений
    """
    def __init__(self, command_config: str, user_state_class: StatesGroup, user_state_data: UserData):
        self.__command_data = dict()
        self.__command_config = command_config
        self.__state_class = user_state_class
        self.__user_state_data = user_state_data
        self.__filter_value = 'PRICE'

    def set_filter_value(self, new_val: str) -> None:
        self.__filter_value = new_val

    def command_from_menu(self, message: Message) -> None:
        bot.set_state(message.from_user.id, self.__state_class.city, message.chat.id)
        bot.send_message(message.from_user.id, self.__command_config['command_welcome_mes'])
        bot.send_message(message.from_user.id, 'Шаг 1 из 3: Введите город')
        self.__command_data[message.chat.id] = self.__user_state_data

    def set_message_handler(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class
        USER_STATE_DATA = self.__user_state_data

        @bot.message_handler(commands=[CUR_COMMAND['command_name']])
        def command(message: Message) -> None:
            bot.set_state(message.from_user.id, CUR_STATE.city, message.chat.id)
            bot.send_message(message.from_user.id, self.__command_config['command_welcome_mes'])
            bot.send_message(message.from_user.id, 'Шаг 1 из 3: Введите город')
            self.__command_data[message.chat.id] = USER_STATE_DATA

    def set_get_city_handler(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class

        @bot.message_handler(state=CUR_STATE.city)
        def get_city(message: Message) -> None:
            towns_ru, towns_en = get_complete_town_name(message.text)
            if towns_ru is not None:
                if len(towns_ru) == 1:
                    self.set_town(message, self.__command_data, towns_ru[0], towns_en[0])
                    self.step_after_town_choose(message)
                else:
                    keyboard = get_town_choose_keyboard(CUR_COMMAND['town_choose_kbrd_key'], towns_ru, towns_en)
                    mes = bot.send_message(message.from_user.id,
                                     'Нет точного совпадения с имеющимися в базе городами, уточните город из предложенных. Если возможна ошибка ввода, введите город ещё раз',
                                     reply_markup=keyboard)
                    self.__command_data[message.chat.id].town_keyboard_message_id = mes.message_id

            else:
                bot.send_message(chat_id=message.chat.id, text='У меня в базе нет такого города, поиск выполнить не получится. Возможно ввод с ошибкой. Введите город ещё раз')
                bot.set_state(message.from_user.id, CUR_STATE.city, message.chat.id)

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
                                  text='Вы выбрали максимальное количество отелей показа за раз: {}'.format(pages_cnt))
            bot.send_message(chat_id=call.message.chat.id, text='Шаг 3 из 3: загружать фото отелей?', reply_markup=keyboard)
            bot.set_state(call.message.from_user.id, CUR_STATE.image_choose, call.message.chat.id)

    def set_hotels_show_image_choose_callback(self) -> None:
        CUR_COMMAND = self.__command_config
        CUR_STATE = self.__state_class

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['image_dialog_key'])
        def hotels_show_image_choose(call: CallbackQuery) -> None:
            if call.data.split('#')[1] == 'yes':
                self.__command_data[call.message.chat.id].image_choose = True

                keyboard = get_hotels_numbers_choose_keyboard(CUR_COMMAND['image_pages_number_key'], [1, 2, 3])
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text='Шаг 3 из 3: выберите сколько фото показывать для каждого отеля',
                                      reply_markup=keyboard)
                bot.set_state(call.message.from_user.id, CUR_STATE.max_images_cnt, call.message.chat.id)
            else:
                self.__command_data[call.message.chat.id].image_choose = False
                mes = self.get_info_message(self.__command_data, call.message.chat.id)
                bot.send_message(chat_id=call.message.chat.id, text=mes)
                bot.delete_state(call.message.from_user.id, call.message.chat.id)
                self.load_data(call.message.chat.id, self.__command_data)

    def set_hotels_show_image_cnt_callback(self) -> None:
        CUR_COMMAND = self.__command_config

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['image_pages_number_key'])
        def hotels_show_image_cnt(call: CallbackQuery) -> None:
            max_images_cnt = int(call.data.split('#')[1])
            self.__command_data[call.message.chat.id].max_image_index = max_images_cnt

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Вы выбрали показывать по {0} фото для отеля'.format(max_images_cnt))

            mes = self.get_info_message(self.__command_data, call.message.chat.id)
            bot.send_message(chat_id=call.message.chat.id, text=mes)
            bot.delete_state(call.message.from_user.id, call.message.chat.id)
            self.load_data(call.message.chat.id, self.__command_data)

    def set_hotel_page_callback(self) -> None:
        CUR_COMMAND = self.__command_config

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['hotels_kbrd_page_key'])
        def hotel_page_callback(call: CallbackQuery) -> None:
            page_ind = int(call.data.split('#')[1])
            if not (page_ind == self.__command_data[call.message.chat.id].cur_page_index):
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

    def get_info_message(self, data_storage: dict, chat_id: int) -> None:
        pages_cnt = data_storage[chat_id].max_page_index
        city = data_storage[chat_id].city_ru
        mes = "Все данные получены. Выбраны следующие параметры запроса:\n\n"
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
                             text='Вы выбрали город: {0}'.format(town))
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='Совпадение с одним городом в базе. Поиск будет выполнен для города: {0}'.format(town))

    def step_after_town_choose(self, message: Message):
        bot.set_state(message.from_user.id, self.__state_class.hotels_number, message.chat.id)
        self.hotels_cnt_choose_step(message)

    def hotels_cnt_choose_step(self, message: Message):
        keyboard = get_hotels_numbers_choose_keyboard(self.__command_config['hotels_pages_number_key'],
                                                      [1, 5, 10, 15])
        bot.send_message(message.chat.id, 'Шаг 2 из 3: выберите сколько отелей показывать в выдаче',
                         reply_markup=keyboard)

    def load_data(self, chat_id: int, data_storage: dict) -> None:
        town = data_storage[chat_id].city_en
        #####################
        hotels_cnt = get_hotel_data_from_server(chat_id, town, data_storage[chat_id].max_page_index, self.__filter_value)
        #####################
        if hotels_cnt > 0:
            if hotels_cnt < data_storage[chat_id].max_page_index:
                data_storage[chat_id].max_page_index = hotels_cnt

            bot.send_message(chat_id=chat_id, text="Доступно отелей для просмотра: {}".format(hotels_cnt))
            image_choose = data_storage[chat_id].image_choose
            if image_choose:
                max_images_cnt = data_storage[chat_id].max_image_index
                for hotel_ind in range(1, hotels_cnt + 1):
                    images_cnt = get_images_links_from_server(get_hotel(chat_id, hotel_ind), max_images_cnt)
                    bot.send_message(chat_id=chat_id,
                                     text="получено изображений для отеля №{0}: {1}".format(hotel_ind, images_cnt))

            page_ind = 1
            image_ind = 1
            change_hotel_page(chat_id,
                              page_ind,
                              image_ind,
                              True,
                              data_storage,
                              self.__command_config['hotels_kbrd_page_key'],
                              self.__command_config['image_kbrd_page_key'])
        else:
            bot.send_message(chat_id=chat_id, text="Нет отелей для просмотра")

    def set_handlers(self) -> None:
        self.set_message_handler()
        self.set_get_city_handler() #self.__state_class.hotels_number)

    def set_callbacks(self) -> None:
        self.set_hotels_page_callback()
        self.set_hotels_show_image_choose_callback()
        self.set_hotels_show_image_cnt_callback()
        self.set_hotel_page_callback()
        self.set_hotel_image_callback()
        self.set_town_callback()

