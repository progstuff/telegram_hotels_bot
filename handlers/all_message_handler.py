from loader import bot
from config_data.config import LOW_PRICE_COMMAND
from handlers.custom_handlers.lowprice import lowprice_handlers
from telebot.types import Message


@bot.message_handler(func=lambda message: True)
def lowprice_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description']:
        lowprice_handlers.lowprice(message)
