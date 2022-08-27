from loader import bot
from config_data.config import LOW_PRICE_COMMAND, HIGH_PRICE_COMMAND, BEST_DEAL_COMMAND
from handlers.custom_handlers.lowprice import LowpriceCommand
from handlers.custom_handlers.highprice import HighpriceCommand
from handlers.custom_handlers.bestdeal import BestDealCommand
from states.user_data_information import UserHighPriceState, UserLowPriceState, UserBestDealState, UserData
from telebot.types import Message

highprice_handlers = HighpriceCommand(HIGH_PRICE_COMMAND, UserHighPriceState, UserData())
highprice_handlers.set_handlers()
highprice_handlers.set_callbacks()

lowprice_handlers = LowpriceCommand(LOW_PRICE_COMMAND, UserLowPriceState, UserData())
lowprice_handlers.set_handlers()
lowprice_handlers.set_callbacks()

bestdeal_handlers = BestDealCommand(BEST_DEAL_COMMAND, UserBestDealState, UserData())
bestdeal_handlers.set_callbacks()
bestdeal_handlers.set_handlers()


@bot.message_handler(state='*')
def command_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description'] or message.text == ('/'+LOW_PRICE_COMMAND['command_name']):
        print('lowprice')
        lowprice_handlers.command_from_menu(message)
    if message.text == HIGH_PRICE_COMMAND['command_description'] or message.text == ('/'+HIGH_PRICE_COMMAND['command_name']):
        print('highprice')
        highprice_handlers.command_from_menu(message)
    if message.text == BEST_DEAL_COMMAND['command_description'] or message.text == ('/'+BEST_DEAL_COMMAND['command_name']):
        print('bestprice')
        bestdeal_handlers.command_from_menu(message)


lowprice_handlers.set_command_invoke_func(command_message)
highprice_handlers.set_command_invoke_func(command_message)
bestdeal_handlers.set_command_invoke_func(command_message)
