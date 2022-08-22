from states.lowprice_information import UserState, UserData
from config_data.config import LOW_PRICE_COMMAND
from handlers.custom_handlers.BaseClassCommand import BaseCommandHandlers


class LowpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config, user_state_class, user_state_data):
        super().__init__(command_config, user_state_class, user_state_data)


lowprice_handlers = LowpriceCommand(LOW_PRICE_COMMAND, UserState, UserData())
lowprice_handlers.set_message_handlers()
lowprice_handlers.set_callback_handlers()