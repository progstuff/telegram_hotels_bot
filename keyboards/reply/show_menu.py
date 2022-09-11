from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from config_data.config import (BEST_DEAL_COMMAND, HELP_COMMAND,
                                HIGH_PRICE_COMMAND, HISTORY_COMMAND,
                                LOW_PRICE_COMMAND)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text=LOW_PRICE_COMMAND['command_description']),
                 KeyboardButton(text=HIGH_PRICE_COMMAND['command_description']))
    keyboard.add(KeyboardButton(text=BEST_DEAL_COMMAND['command_description']),
                 KeyboardButton(text=HISTORY_COMMAND['command_description']))

    return keyboard
