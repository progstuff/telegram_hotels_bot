from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config_data.config import CUSTOM_COMMANDS


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for command, description in CUSTOM_COMMANDS:
        keyboard.add(InlineKeyboardButton(text=description, callback_data=command))
    return keyboard
