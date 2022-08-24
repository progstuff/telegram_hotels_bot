from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_price_choose_keyboard(key_data: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='до 200$', callback_data='{0}#{1}'.format(key_data, 1)))
    keyboard.add(InlineKeyboardButton(text='от 200$ до 500$', callback_data='{0}#{1}'.format(key_data, 2)))
    keyboard.add(InlineKeyboardButton(text='от 500$ до 1000$', callback_data='{0}#{1}'.format(key_data, 3)))
    keyboard.add(InlineKeyboardButton(text='свыше 1000$', callback_data='{0}#{1}'.format(key_data, 4)))
    return keyboard


