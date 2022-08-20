import telebot


def get_town_choose_keyboard(key_data, values_ru, values_en):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for val_ru, val_en in zip(values_ru, values_en):
        keyboard.add(telebot.types.InlineKeyboardButton(text=str(val_ru), callback_data='{0}#{1}'.format(key_data, val_en)))
    return keyboard
