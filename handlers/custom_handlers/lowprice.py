from handlers.custom_handlers.base_command_class import BaseCommandHandlers
from states.user_data_information import StatesGroup


class LowpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup):
        super().__init__(command_config, user_state_class)
        self.calendar_id = "lowprice"


