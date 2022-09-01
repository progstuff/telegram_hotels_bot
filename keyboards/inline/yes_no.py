from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_yes_no_keyboard(prefix: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(text='Да', callback_data='{}#yes'.format(prefix))
    button_no = InlineKeyboardButton(text='Нет', callback_data='{}#no'.format(prefix))
    keyboard.row(button_yes, button_no)
    return keyboard
