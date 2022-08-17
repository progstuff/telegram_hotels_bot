from loader import bot
from keyboards.inline.hotels_chooser import get_lowprice_paginator
from db.hotels_parser import get_lowprice_data_from_server
from db.hotels_parser import get_lowprice_hotel_data
from handlers.custom_handlers.lowprice import lowprice_data


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page_numbers')
def hotels_page_callback(call):
    pages_cnt = int(call.data.split('#')[1])
    print('here')

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    bot.send_message(chat_id=call.message.chat.id, text='Все данные получены, начинаю загрузку отелей')

    #get_lowprice_data_from_server()
    #with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
    lowprice_data[call.message.chat.id].hotels_number = pages_cnt
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