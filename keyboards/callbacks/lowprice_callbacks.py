from loader import bot
from keyboards.inline.hotels_chooser import get_lowprice_paginator
from db.hotels_parser import get_lowprice_data_from_server
from db.hotels_parser import get_lowprice_hotel_data
from handlers.custom_handlers.lowprice import lowprice_data
from states.lowprice_information import UserLowPriceState
from keyboards.inline.yes_no import get_yes_no_keyboard


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page_numbers')
def hotels_page_callback(call):
    pages_cnt = int(call.data.split('#')[1])
    lowprice_data[call.message.chat.id].hotels_number = pages_cnt
    keyboard = get_yes_no_keyboard('lowprice_image_choose')

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Вы выбрали максимальное количество отелей показа за раз: {}'.format(pages_cnt))
    bot.send_message(chat_id=call.message.chat.id, text='Шаг 3 из 3: загружать фото отелей?', reply_markup=keyboard)
    bot.set_state(call.message.from_user.id, UserLowPriceState.image_choose, call.message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_image_choose')
def hotels_show_image_choose(call):
    image_choose = 'без фото'
    if call.data.split('#')[1] == 'yes':
        image_choose = 'с фото'
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Вы выбрали показ отелей: {}'.format(image_choose))
    pages_cnt = lowprice_data[call.message.chat.id].hotels_number
    city = lowprice_data[call.message.chat.id].city
    mes = """Все данные получены. Выбраны следующие параметры запроса:\n
    \tгород: {0}
    \tколичество отелей в выдаче: {1}
    \tпоказ изображений: {2}\n
Начинаю загрузку отелей
    """.format(city, pages_cnt, image_choose)
    bot.send_message(chat_id=call.message.chat.id, text=mes)

    # get_lowprice_data_from_server()
    bot.delete_state(call.message.from_user.id, call.message.chat.id)
    # тут должно быть обращение к БД
    hotel_data = get_lowprice_hotel_data(0)

    paginator = get_lowprice_paginator(0, pages_cnt)
    bot.send_message(
        call.message.chat.id,
        hotel_data,
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page')
def hotel_page_callback(call):
    page = int(call.data.split('#')[1])
    pages_cnt = lowprice_data[call.message.chat.id].hotels_number
    paginator = get_lowprice_paginator(page, pages_cnt)
    hotel_data = get_lowprice_hotel_data(page - 1)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=hotel_data, reply_markup=paginator.markup)