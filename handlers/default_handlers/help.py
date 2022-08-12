from telebot.types import Message

from loader import bot
from config_data.config import HELP_MESSAGE


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    bot.send_message(message.chat.id, HELP_MESSAGE)
