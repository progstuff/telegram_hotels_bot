from states.user_data_information import UserData, StatesGroup
from handlers.custom_handlers.base_command_class import BaseCommandHandlers


class LowpriceCommand(BaseCommandHandlers):

    def __init__(self, command_config: str, user_state_class: StatesGroup, user_state_data: UserData):
        super().__init__(command_config, user_state_class, user_state_data)
        self.calendar_id = "lowprice"


