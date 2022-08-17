from telebot.types import Message
from keyboards.reply.show_menu import get_main_menu_keyboard
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    main_menu_keyboard = get_main_menu_keyboard()
    bot.send_message(message.chat.id, "Какие отели Вас интересуют?", reply_markup=main_menu_keyboard)
