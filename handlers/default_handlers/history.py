from telebot.types import Message

from loader import bot
from config_data.config import HISTORY_COMMAND


def bot_history(message: Message) -> None:
    bot.send_message(message.chat.id, HISTORY_COMMAND['command_welcome_mes'])
