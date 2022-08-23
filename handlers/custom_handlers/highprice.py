from states.lowprice_information import UserHighPriceState, UserData
from config_data.config import HIGH_PRICE_COMMAND
from handlers.custom_handlers.BaseClassCommand import BaseCommandHandlers


class HighpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config, user_state_class, user_state_data):
        super().__init__(command_config, user_state_class, user_state_data)
        self.set_filter_value('PRICE_HIGHEST_FIRST')


highprice_handlers = HighpriceCommand(HIGH_PRICE_COMMAND, UserHighPriceState, UserData())
highprice_handlers.set_handlers()
highprice_handlers.set_callbacks()
