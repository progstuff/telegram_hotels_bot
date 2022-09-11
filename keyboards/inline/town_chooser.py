from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_town_choose_keyboard(key_data: str, values_ru: str, values_en: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for val_ru, val_en in zip(values_ru, values_en):
        keyboard.add(InlineKeyboardButton(text=str(val_ru), callback_data='{0}#{1}'.format(key_data, val_en)))
    return keyboard
