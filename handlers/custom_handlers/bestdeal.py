from states.user_data_information import UserBestDealState, UserData, StatesGroup
from config_data.config import BEST_DEAL_COMMAND
from handlers.custom_handlers.base_command_class import BaseCommandHandlers
from keyboards.inline.price_choose import get_price_choose_keyboard
from telebot.types import Message
from loader import bot
from telebot.types import CallbackQuery


class BestDealCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup, user_state_data: UserData):
        super().__init__(command_config, user_state_class, user_state_data)
        self.set_filter_value('PRICE_HIGHEST_FIRST')
        self.set_max_steps_cnt(5)
        self.__price_vals = [200, 500, 1000]

    def step_after_town_choose(self, message: Message):
        bot.set_state(message.from_user.id, self.state_class.hotels_price, message.chat.id)
        self.price_choose_step(message)

    def price_choose_step(self, message: Message):
        keyboard = get_price_choose_keyboard(self.command_config['hotels_price_key'], self.__price_vals)
        mes = bot.send_message(message.chat.id,
                         'Шаг {0} из {1}: выберите диапазон цен'.format(self.cur_step, self.max_steps_cnt),
                         reply_markup=keyboard)
        self.command_data[mes.chat.id].price_keyboard_message_id = mes.message_id
        self.increase_step()


    def set_price_choose_handler(self):
        CUR_STATE = self.state_class

        @bot.message_handler(state=CUR_STATE.hotels_price)
        def get_price(message: Message) -> None:
            bot.send_message(message.chat.id, 'Выберите из предложенных диапазонов цен')
            bot.delete_message(message.chat.id, self.command_data[message.chat.id].price_keyboard_message_id)
            keyboard = get_price_choose_keyboard(self.command_config['hotels_price_key'], )
            mes = bot.send_message(message.chat.id,
                                   'Шаг {0} из {1}: выберите диапазон цен'.format(self.cur_step, self.max_steps_cnt),
                                   reply_markup=keyboard)
            self.command_data[mes.chat.id].price_keyboard_message_id = mes.message_id

    def set_distance_callback(self):
        CUR_COMMAND = self.command_config

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['distance_choose_key'])
        def distance_choose_callback(call: CallbackQuery) -> None:
            pass

    def set_price_choose_callback(self):
        CUR_COMMAND = self.command_config
        CUR_STATE = self.state_class

        @bot.callback_query_handler(func=lambda call: call.data.split('#')[0] == CUR_COMMAND['hotels_price_key'])
        def price_choose_callback(call: CallbackQuery) -> None:
            price_range_index = int(call.data.split('#')[1])
            max_price = -1
            if price_range_index == 0:
                min_price = 0
                max_price = self.__price_vals[0]
            elif price_range_index == len(self.__price_vals):
                min_price = self.__price_vals[-1]
            else:
                min_price = self.__price_vals[price_range_index-1]
                max_price = self.__price_vals[price_range_index]
            self.command_data[call.message.chat.id].min_price = min_price
            self.command_data[call.message.chat.id].max_price = max_price
            message_text = call.data.split('#')[2]
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=self.command_data[call.message.chat.id].price_keyboard_message_id)
            bot.send_message(call.message.chat.id, 'вы выбрали диапазон цен: ' + message_text)
            bot.set_state(call.message.from_user.id, CUR_STATE.distance_to_center, call.message.chat.id)

    def set_handlers(self) -> None:
        self.set_message_handler()
        self.set_get_city_handler()
        self.set_price_choose_handler()

    def set_callbacks(self) -> None:
        self.set_hotels_page_callback()
        self.set_hotels_show_image_choose_callback()
        self.set_hotels_show_image_cnt_callback()
        self.set_hotel_page_callback()
        self.set_hotel_image_callback()
        self.set_town_callback()
        self.set_price_choose_callback()

    #def set_price_handler(self):
    #    @bot.message_handler(state=CUR_STATE.city)
    #    def get_city(message: Message) -> None:


bestdeal_handlers = BestDealCommand(BEST_DEAL_COMMAND, UserBestDealState, UserData())
bestdeal_handlers.set_handlers()
bestdeal_handlers.set_callbacks()
