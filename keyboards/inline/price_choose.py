from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_price_choose_keyboard(key_data: str, price_vals: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button_text = 'до {}$'.format(price_vals[0])
    keyboard.add(InlineKeyboardButton(text=button_text,
                                      callback_data='{0}#{1}#{2}'.format(key_data, 0, button_text)))
    for i in range(1, len(price_vals)):
        button_text = 'от {0}$ до {1}$'.format(price_vals[i-1], price_vals[i])
        keyboard.add(InlineKeyboardButton(text=button_text,
                                          callback_data='{0}#{1}#{2}'.format(key_data, i, button_text)))
    button_text = 'свыше {}$'.format(price_vals[-1])
    keyboard.add(InlineKeyboardButton(text=button_text,
                                      callback_data='{0}#{1}#{2}'.format(key_data, len(price_vals), button_text)))
    return keyboard


