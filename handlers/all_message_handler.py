from loader import bot
from config_data.config import LOW_PRICE_COMMAND, HIGH_PRICE_COMMAND
from handlers.custom_handlers.lowprice import lowprice_handlers
from handlers.custom_handlers.highprice import highprice_handlers
from telebot.types import Message


@bot.message_handler(func=lambda message: True)
def command_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description']:
        lowprice_handlers.command_from_menu(message)
    if message.text == HIGH_PRICE_COMMAND['command_description']:
        highprice_handlers.command_from_menu(message)
