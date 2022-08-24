from states.user_data_information import UserHighPriceState, UserData, StatesGroup
from config_data.config import HIGH_PRICE_COMMAND
from handlers.custom_handlers.base_command_class import BaseCommandHandlers

class HighpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup, user_state_data: UserData):
        super().__init__(command_config, user_state_class, user_state_data)
        self.set_filter_value('PRICE_HIGHEST_FIRST')


highprice_handlers = HighpriceCommand(HIGH_PRICE_COMMAND, UserHighPriceState, UserData())
highprice_handlers.set_handlers()
highprice_handlers.set_callbacks()
