from states.user_data_information import UserLowPriceState, UserData, StatesGroup
from config_data.config import LOW_PRICE_COMMAND
from handlers.custom_handlers.base_command_class import BaseCommandHandlers


class LowpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup, user_state_data: UserData):
        super().__init__(command_config, user_state_class, user_state_data)


lowprice_handlers = LowpriceCommand(LOW_PRICE_COMMAND, UserLowPriceState, UserData())
lowprice_handlers.set_handlers()
lowprice_handlers.set_callbacks()