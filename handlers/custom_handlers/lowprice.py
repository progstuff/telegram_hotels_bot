from loader import bot
from telebot.types import Message
from config_data.config import LOW_PRICE_COMMAND


@bot.message_handler(commands=[LOW_PRICE_COMMAND['command_name']],
                     content_types=[LOW_PRICE_COMMAND['command_description']])
def lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id, 'вы выбрали показать топ самых дешевых отелей в городе. Введите город')