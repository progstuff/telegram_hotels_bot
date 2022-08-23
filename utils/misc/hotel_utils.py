from loader import bot
from keyboards.inline.hotels_chooser import hotels_paginator, get_photo_keyboard
from db.hotels_parser import get_db_hotel_data, get_hotel_image
from telebot.types import InputMedia
from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery
from telegram_bot_pagination import InlineKeyboardPaginator

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
    paginator = hotels_paginator(page, pages_cnt, hotel_kbrd_key)
    is_need_images = data_storage[chat_id].image_choose
    photo_keyboard = None
    if is_need_images:
        data_storage[chat_id].cur_image_index = image_index
        cur_image_index = data_storage[chat_id].cur_image_index
        max_image_index = data_storage[chat_id].max_image_index
        photo_keyboard = get_photo_keyboard(cur_image_index, max_image_index, image_kbrd_key)

    hotel_data = get_db_hotel_data(chat_id, page - 1)
    if is_first:
        send_hotel_message(chat_id, hotel_data, paginator, photo_keyboard, is_need_images, data_storage)
    else:
        update_hotel_message(chat_id, hotel_data, paginator, photo_keyboard, is_need_images, data_storage)


def send_hotel_message(chat_id: int, hotel_data: dict, paginator: InlineKeyboardPaginator, photo_keyboard: str, is_need_images: bool, data_storage: dict) -> None:
    if is_need_images:
        image_index = data_storage[chat_id].cur_image_index
        page_index = data_storage[chat_id].cur_page_index
        if photo_keyboard is not None:
            sended_message = bot.send_photo(
                chat_id=chat_id,
                photo=get_hotel_image(chat_id, page_index, image_index),
                reply_markup=photo_keyboard
            )
        else:
            sended_message = bot.send_photo(
                chat_id=chat_id,
                photo=get_hotel_image(chat_id, page_index, image_index)
            )
        data_storage[sended_message.chat.id].photo_message_id = sended_message.id
    sended_message = bot.send_message(
        chat_id,
        text=hotel_data,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )
    data_storage[sended_message.chat.id].text_message_id = sended_message.id


def update_hotel_message(chat_id: int, hotel_data: dict, paginator: InlineKeyboardPaginator, photo_keyboard: str, is_need_images: bool, data_storage: dict):
    if is_need_images:
        try:
            image_index = data_storage[chat_id].cur_image_index
            page_index = data_storage[chat_id].cur_page_index
            if photo_keyboard is not None:
                bot.edit_message_media(
                    media=InputMedia(type='photo',
                                     media=get_hotel_image(chat_id, page_index, image_index)),
                    chat_id=chat_id,
                    reply_markup=photo_keyboard,
                    message_id=data_storage[chat_id].photo_message_id
                )
            else:
                bot.edit_message_media(
                    media=InputMedia(type='photo',
                                     media=get_hotel_image(chat_id, page_index, image_index)),
                    chat_id=chat_id,
                    message_id=data_storage[chat_id].photo_message_id
                )

        except ApiTelegramException:
            print('фото без изменений')
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=data_storage[chat_id].text_message_id,
            text=hotel_data,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
    except ApiTelegramException:
        print('текст без изменений')