from loader import bot
from config_data.config import HOTEL_PAGES # тут должна быть БД
from keyboards.inline.hotels_chooser import get_lowprice_paginator


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page_numbers')
def hotels_page_callback(call):
    number = int(call.data.split('#')[1])
    print('here')
    bot.send_message(chat_id=call.message.chat.id, text='Все данные получены, начинаю загрузку отелей')
    bot.delete_state(call.message.from_user.id, call.message.chat.id)

    # тут должно быть обращение к БД

    paginator = get_lowprice_paginator(0)
    bot.send_message(
        call.message.chat.id,
        HOTEL_PAGES[0],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page')
def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    #bot.delete_message(
    #    call.message.chat.id,
    #    call.message.message_id
    #)
    paginator = get_lowprice_paginator(page)
    bot.send_message(
        call.message.chat.id,
        HOTEL_PAGES[page - 1],
        reply_markup=paginator.markup,
        parse_mode='Markdown'
    )