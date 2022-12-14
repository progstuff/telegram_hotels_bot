from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, InputMedia
from telegram_bot_pagination import InlineKeyboardPaginator

from keyboards.inline.hotels_chooser import (get_photo_keyboard,
                                             hotels_paginator)
from loader import bot
from loguru import logger


# одинаковый код для lowprice, highprice
def hotel_image_slide_photo(call: CallbackQuery, data_storage: dict, hotel_kbrd_key: str, image_kbrd_key: str) -> None:
    type_btn = call.data.split('#')[1]
    if type_btn != 'cur':
        prev_image_ind = data_storage[call.message.chat.id].cur_image_index
        if type_btn == 'prev':
            data_storage[call.message.chat.id].cur_image_index -= 1
        elif type_btn == 'next':
            data_storage[call.message.chat.id].cur_image_index += 1

        image_ind = data_storage[call.message.chat.id].cur_image_index
        if not (prev_image_ind == image_ind):
            page_ind = data_storage[call.message.chat.id].cur_page_index
            change_hotel_page(call.message.chat.id, page_ind, image_ind, False, data_storage, hotel_kbrd_key, image_kbrd_key)


def change_hotel_page(chat_id: int, page: int, image_index: int, is_first: bool, data_storage: dict, hotel_kbrd_key: str, image_kbrd_key: str):
    data_storage[chat_id].cur_page_index = page
    pages_cnt = data_storage[chat_id].max_page_index
    cur_global_page_ind = data_storage[chat_id].cur_global_page_ind
    max_global_page_ind = data_storage[chat_id].max_global_page_ind
    paginator = hotels_paginator(page, pages_cnt, cur_global_page_ind, max_global_page_ind, hotel_kbrd_key)
    is_need_images = data_storage[chat_id].image_choose
    photo_keyboard = None
    if is_need_images:
        data_storage[chat_id].cur_image_index = image_index
        cur_image_index = data_storage[chat_id].cur_image_index
        max_image_index = data_storage[chat_id].hotels_data.get_links_cnt(page)
        photo_keyboard = get_photo_keyboard(cur_image_index, max_image_index, image_kbrd_key)

    local_hotels_data = data_storage[chat_id].hotels_data
    hotel_data = local_hotels_data.get_db_hotel_data(page - 1)
    if is_first:
        send_hotel_message(chat_id, hotel_data, paginator, photo_keyboard, is_need_images, data_storage)
    else:
        update_hotel_message(chat_id, hotel_data, paginator, photo_keyboard, is_need_images, data_storage)


def send_hotel_message(chat_id: int, hotel_data: dict, paginator: InlineKeyboardPaginator, photo_keyboard: str, is_need_images: bool, data_storage: dict) -> None:
    if is_need_images:
        image_index = data_storage[chat_id].cur_image_index
        page_index = data_storage[chat_id].cur_page_index
        local_hotels_data = data_storage[chat_id].hotels_data
        if photo_keyboard is not None:
            sended_message = bot.send_photo(
                chat_id=chat_id,
                photo=local_hotels_data.get_hotel_image(page_index, image_index),
                reply_markup=photo_keyboard
            )
        else:
            sended_message = bot.send_photo(
                chat_id=chat_id,
                photo=local_hotels_data.get_hotel_image(page_index, image_index)
            )
        data_storage[sended_message.chat.id].photo_message_id = sended_message.id
    sended_message = bot.send_message(
        chat_id,
        text=hotel_data,
        reply_markup=paginator.markup,
        disable_web_page_preview=True,
        parse_mode='Markdown'
    )
    data_storage[sended_message.chat.id].text_message_id = sended_message.id


def update_hotel_message(chat_id: int, hotel_data: dict, paginator: InlineKeyboardPaginator, photo_keyboard: str, is_need_images: bool, data_storage: dict):
    if is_need_images:
        try:
            image_index = data_storage[chat_id].cur_image_index
            page_index = data_storage[chat_id].cur_page_index
            local_hotels_data = data_storage[chat_id].hotels_data
            if photo_keyboard is not None:
                bot.edit_message_media(
                    media=InputMedia(type='photo',
                                     media=local_hotels_data.get_hotel_image(page_index, image_index)),
                    chat_id=chat_id,
                    reply_markup=photo_keyboard,
                    message_id=data_storage[chat_id].photo_message_id
                )
            else:
                bot.edit_message_media(
                    media=InputMedia(type='photo',
                                     media=local_hotels_data.get_hotel_image(page_index, image_index)),
                    chat_id=chat_id,
                    message_id=data_storage[chat_id].photo_message_id
                )

        except ApiTelegramException:
            logger.warning('чат - {0}: переключение фото отеля - фото без изменений'.format(chat_id))
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=data_storage[chat_id].text_message_id,
            text=hotel_data,
            reply_markup=paginator.markup,
            disable_web_page_preview=True,
            parse_mode='Markdown'
        )
    except ApiTelegramException:
        logger.warning('чат - {0}: переключение описания отеля - текст без изменений'.format(chat_id))