import telebot
from telegram_bot_pagination import InlineKeyboardPaginator

def get_hotels_numbers_choose_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='lowprice_page_numbers#1')
    button5 = telebot.types.InlineKeyboardButton(text='5', callback_data='lowprice_page_numbers#5')
    button10 = telebot.types.InlineKeyboardButton(text='10', callback_data='lowprice_page_numbers#10')
    button15 = telebot.types.InlineKeyboardButton(text='15', callback_data='lowprice_page_numbers#15')
    keyboard.row(button1, button5, button10, button15)
    return keyboard

def get_lowprice_paginator(page):
    paginator = InlineKeyboardPaginator(
        10,
        current_page=page,
        data_pattern='lowprice_page#{page}'
    )
    return paginator

