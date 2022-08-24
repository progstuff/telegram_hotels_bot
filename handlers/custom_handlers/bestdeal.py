from states.user_data_information import UserBestDealState, UserData
from config_data.config import BEST_DEAL_COMMAND
from handlers.custom_handlers.base_command_class import BaseCommandHandlers
from keyboards.inline.price_choose import get_price_choose_keyboard
from telebot.types import Message
from loader import bot
from states.user_data_information import UserData, StatesGroup


class BestDealCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup, user_state_data: UserData):
        super().__init__(command_config, user_state_class, user_state_data)
        self.set_filter_value('PRICE_HIGHEST_FIRST')
        self.set_max_steps_cnt(5)

    def step_after_town_choose(self, message: Message):
        bot.set_state(message.from_user.id, self.state_class.hotels_price, message.chat.id)
        self.price_choose_step(message)

    def price_choose_step(self, message: Message):
        keyboard = get_price_choose_keyboard(self.command_config['hotels_price_key'],)
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

    def set_handlers(self) -> None:
        self.set_message_handler()
        self.set_get_city_handler()
        self.set_price_choose_handler()

    #def set_price_handler(self):
    #    @bot.message_handler(state=CUR_STATE.city)
    #    def get_city(message: Message) -> None:


bestdeal_handlers = BestDealCommand(BEST_DEAL_COMMAND, UserBestDealState, UserData())
bestdeal_handlers.set_handlers()
bestdeal_handlers.set_callbacks()
