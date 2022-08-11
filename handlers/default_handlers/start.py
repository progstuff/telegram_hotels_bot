from telebot.types import Message
from keyboards.inline.show_menu import get_main_menu_keyboard
from loader import bot
from keyboards.callbacks.callback_utils import get_answer_object


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    main_menu_keyboard = get_main_menu_keyboard()
    bot.send_message(message.chat.id, "Чем я могу помочь?", reply_markup=main_menu_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    callback_answer_object = get_answer_object(call.data)
    result, answer = callback_answer_object.return_answer()

    if result:
        bot.send_message(call.message.chat.id, answer)
