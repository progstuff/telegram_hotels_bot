from loader import bot
from keyboards.inline.hotels_chooser import hotels_paginator, add_photo_buttons
from db.hotels_parser import get_lowprice_data_from_server
from db.hotels_parser import get_lowprice_hotel_data
from handlers.custom_handlers.lowprice import lowprice_data
from states.lowprice_information import UserLowPriceState
from keyboards.inline.yes_no import get_yes_no_keyboard


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page_numbers')
def hotels_page_callback(call):
    pages_cnt = int(call.data.split('#')[1])
    lowprice_data[call.message.chat.id].max_page_index = pages_cnt
    keyboard = get_yes_no_keyboard('lowprice_image_choose')

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Вы выбрали максимальное количество отелей показа за раз: {}'.format(pages_cnt))
    bot.send_message(chat_id=call.message.chat.id, text='Шаг 3 из 3: загружать фото отелей?', reply_markup=keyboard)
    bot.set_state(call.message.from_user.id, UserLowPriceState.image_choose, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_image_choose')
def hotels_show_image_choose(call):
    is_need_images = False
    image_choose = 'без фото'
    if call.data.split('#')[1] == 'yes':
        image_choose = 'с фото'
        is_need_images = True
    lowprice_data[call.message.chat.id].image_choose = is_need_images

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Вы выбрали показ отелей: {}'.format(image_choose))
    pages_cnt = lowprice_data[call.message.chat.id].max_page_index
    city = lowprice_data[call.message.chat.id].city
    mes = """Все данные получены. Выбраны следующие параметры запроса:\n
    \tгород: {0}
    \tколичество отелей в выдаче: {1}
    \tпоказ изображений: {2}\n
Начинаю загрузку отелей
    """.format(city, pages_cnt, image_choose)
    bot.send_message(chat_id=call.message.chat.id, text=mes)

    #get_lowprice_data_from_server()
    bot.delete_state(call.message.from_user.id, call.message.chat.id)
    # тут должно быть обращение к БД
    page_ind = 1
    image_ind = 1
    change_page(call, page_ind, image_ind, True)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page')
def hotel_page_callback(call):
    page_ind = int(call.data.split('#')[1])
    if not(page_ind == lowprice_data[call.message.chat.id].cur_page_index):
        image_ind = 1
        change_page(call, page_ind, image_ind, False)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_image')
def hotel_image_callback(call):
    type_btn = call.data.split('#')[1]
    if type_btn != 'cur':
        prev_image_ind = lowprice_data[call.message.chat.id].cur_image_index
        if type_btn == 'prev':
            lowprice_data[call.message.chat.id].cur_image_index -= 1
        elif type_btn == 'next':
            lowprice_data[call.message.chat.id].cur_image_index += 1

        image_ind = lowprice_data[call.message.chat.id].cur_image_index
        if not(prev_image_ind == image_ind):
            page_ind = lowprice_data[call.message.chat.id].cur_page_index
            change_page(call, page_ind, image_ind, False)


def change_page(call, page, image_index, is_first):
    lowprice_data[call.message.chat.id].cur_page_index = page
    pages_cnt = lowprice_data[call.message.chat.id].max_page_index
    paginator = hotels_paginator(page, pages_cnt, 'lowprice_page')
    is_need_images = lowprice_data[call.message.chat.id].image_choose
    if is_need_images:
        lowprice_data[call.message.chat.id].cur_image_index = image_index
        cur_image_index = lowprice_data[call.message.chat.id].cur_image_index
        max_image_index = lowprice_data[call.message.chat.id].max_image_index
        add_photo_buttons(paginator, cur_image_index, max_image_index, 'lowprice_image')
    hotel_data = get_lowprice_hotel_data(page-1)
    if is_first:
        bot.send_message(
            call.message.chat.id,
            hotel_data,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=hotel_data,
            reply_markup=paginator.markup,
            parse_mode='Markdown'
        )