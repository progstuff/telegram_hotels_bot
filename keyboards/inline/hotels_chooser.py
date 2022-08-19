import telebot
from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton


def get_hotels_numbers_choose_keyboard(key_data, values):
    keyboard = telebot.types.InlineKeyboardMarkup()
    buttons = []
    for val in values:
        buttons.append(telebot.types.InlineKeyboardButton(text=str(val), callback_data='{0}#{1}'.format(key_data, val)))
    keyboard.row(*buttons)
    return keyboard


def hotels_paginator(page, pages_cnt, data_prefix):
    paginator = InlineKeyboardPaginator(
        pages_cnt,
        current_page=page,
        data_pattern=data_prefix + '#{page}'
    )
    return paginator


def get_photo_keyboard(photo_number, photos_numbers, data_prefix):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('<', callback_data=data_prefix + '#prev'),
        InlineKeyboardButton('{0}/{1}'.format(photo_number, photos_numbers), callback_data=data_prefix + '#cur'),
        InlineKeyboardButton('>', callback_data=data_prefix + '#next')
    )
    return keyboard
