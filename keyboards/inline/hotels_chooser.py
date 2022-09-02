from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator


def get_hotels_numbers_choose_keyboard(key_data: str, values: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    buttons = []
    for val in values:
        buttons.append(InlineKeyboardButton(text=str(val), callback_data='{0}#{1}'.format(key_data, val)))
    keyboard.row(*buttons)
    return keyboard


def hotels_paginator(page: int, pages_cnt: int, cur_global_page: int, max_global_pages: int, data_prefix: str) -> InlineKeyboardPaginator:
    paginator = InlineKeyboardPaginator(
        pages_cnt,
        current_page=page,
        data_pattern=data_prefix + '#{page}'
    )
    if cur_global_page == max_global_pages:
        paginator.add_after(InlineKeyboardButton('Предыдущие', callback_data=data_prefix + '#backward'),
                            InlineKeyboardButton('{0}/{1}'.format(cur_global_page, max_global_pages),
                                                 callback_data=data_prefix + '#backward'),
                            InlineKeyboardButton('Загрузить ещё', callback_data=data_prefix + '#forward_web'))
    else:
        paginator.add_after(InlineKeyboardButton('Предыдущие', callback_data=data_prefix + '#backward'),
                            InlineKeyboardButton('{0}/{1}'.format(cur_global_page, max_global_pages),
                                                 callback_data=data_prefix + '#backward'),
                            InlineKeyboardButton('Следующие', callback_data=data_prefix + '#forward'))
    return paginator


def history_hotels_paginator(page: int, pages_cnt: int, cur_global_page: int, max_global_pages: int, data_prefix: str) -> InlineKeyboardPaginator:
    paginator = InlineKeyboardPaginator(
        pages_cnt,
        current_page=page,
        data_pattern=data_prefix + '#{page}'
    )
    paginator.add_after(InlineKeyboardButton('Предыдущие', callback_data=data_prefix + '#backward'),
                        InlineKeyboardButton('{0}/{1}'.format(cur_global_page, max_global_pages),
                                             callback_data=data_prefix + '#backward'),
                        InlineKeyboardButton('Следующие', callback_data=data_prefix + '#forward'))
    return paginator


def get_photo_keyboard(photo_number: int, photos_numbers: int, data_prefix: str) -> InlineKeyboardMarkup:
    if photos_numbers > 1:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(
            InlineKeyboardButton('<', callback_data=data_prefix + '#prev'),
            InlineKeyboardButton('{0}/{1}'.format(photo_number, photos_numbers), callback_data=data_prefix + '#cur'),
            InlineKeyboardButton('>', callback_data=data_prefix + '#next')
        )
        return keyboard
    return None
