import telebot
from telegram_bot_pagination import InlineKeyboardPaginator
from telebot.types import InlineKeyboardButton


def get_hotels_numbers_choose_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='lowprice_page_numbers#1')
    button5 = telebot.types.InlineKeyboardButton(text='5', callback_data='lowprice_page_numbers#5')
    button10 = telebot.types.InlineKeyboardButton(text='10', callback_data='lowprice_page_numbers#10')
    button15 = telebot.types.InlineKeyboardButton(text='15', callback_data='lowprice_page_numbers#15')
    keyboard.row(button1, button5, button10, button15)
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
