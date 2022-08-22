from states.lowprice_information import UserState, UserData
from config_data.config import HIGH_PRICE_COMMAND
from handlers.custom_handlers.BaseClassCommand import BaseCommandHandlers


class HighpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config, user_state_class, user_state_data):
        super().__init__(command_config, user_state_class, user_state_data)


#highprice_handlers = HighpriceCommand(HIGH_PRICE_COMMAND, UserState, UserData())
#highprice_handlers.set_message_handlers()
#highprice_handlers.set_callback_handlers()