from telebot.types import Message

from loader import bot
from config_data.config import HISTORY_COMMAND
from database.command_history_data import CommandDataDb, UserDataDb, HotelDb


def bot_history(message: Message) -> None:

    command_rows = CommandDataDb.select()
    for row in command_rows:
        user = UserDataDb.get(UserDataDb.id == row.user_id)
        mes = row.get_str_view() + '\n'
        hotels = HotelDb.select().where(HotelDb.command_data == row)
        bot.send_message(message.chat.id, mes)
        for hotel in hotels:
            mes = hotel.get_str_view()
            bot.send_message(message.chat.id, mes)


