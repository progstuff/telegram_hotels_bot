from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id, 'вы выбрали показать топ самых дешевых отелей в городе. Введите город')