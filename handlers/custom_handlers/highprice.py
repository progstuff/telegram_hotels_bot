from handlers.custom_handlers.base_command_class import BaseCommandHandlers
from states.user_data_information import StatesGroup


class HighpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup):
        super().__init__(command_config, user_state_class)
        self.set_filter_value('PRICE_HIGHEST_FIRST')
        self.calendar_id = "highprice"



