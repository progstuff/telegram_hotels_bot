from states.user_data_information import UserBestDealState, UserData
from config_data.config import BEST_DEAL_COMMAND
from handlers.custom_handlers.base_command_class import BaseCommandHandlers
from telebot.types import Message
from loader import bot

class BestDealCommand(BaseCommandHandlers):

    def __init__(self, command_config, user_state_class, user_state_data):
        super().__init__(command_config, user_state_class, user_state_data)
        self.set_filter_value('PRICE_HIGHEST_FIRST')

    def step_after_town_choose(self, message: Message):
        bot.send_message(chat_id=message.chat.id,
                         text='тут будет что-то другое')


bestdeal_handlers = BestDealCommand(BEST_DEAL_COMMAND, UserBestDealState, UserData())
bestdeal_handlers.set_handlers()
bestdeal_handlers.set_callbacks()
