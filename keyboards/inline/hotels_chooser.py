import telebot


def get_hotels_numbers_choose_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='1')
    button5 = telebot.types.InlineKeyboardButton(text='5', callback_data='5')
    button10 = telebot.types.InlineKeyboardButton(text='10', callback_data='10')
    button15 = telebot.types.InlineKeyboardButton(text='15', callback_data='15')
    keyboard.row(button1, button5, button10, button15)
    return keyboard
