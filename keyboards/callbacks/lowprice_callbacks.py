from loader import bot
from handlers.custom_handlers.lowprice import lowprice_data
from states.lowprice_information import UserLowPriceState
from keyboards.inline.yes_no import get_yes_no_keyboard
from utils.misc.hotel_utils import change_hotel_page, hotel_image_slide_photo
from db.hotels_parser import get_lowprice_data_from_server, get_images_links_from_server


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
                          text='Вы выбрали показ отелей {}'.format(image_choose))
    pages_cnt = lowprice_data[call.message.chat.id].max_page_index
    city = lowprice_data[call.message.chat.id].city
    mes = """Все данные получены. Выбраны следующие параметры запроса:\n
    \tгород: {0}
    \tколичество отелей в выдаче: {1}
    \tпоказ отелей {2}\n
Начинаю загрузку отелей
    """.format(city, pages_cnt, image_choose)
    bot.send_message(chat_id=call.message.chat.id, text=mes)

    hotels_cnt = get_lowprice_data_from_server(call.message.chat.id)
    bot.delete_state(call.message.from_user.id, call.message.chat.id)

    if hotels_cnt > 0:
        if hotels_cnt < lowprice_data[call.message.chat.id].max_page_index:
            lowprice_data[call.message.chat.id].max_page_index = hotels_cnt
            bot.send_message(chat_id=call.message.chat.id, text="Доступно отелей для просмотра: {}".format(hotels_cnt))
        if is_need_images:
            get_images_links_from_server(call.message.chat.id)

        #if links is not None:
            #load_image(links[0])

        page_ind = 1
        image_ind = 1
        change_hotel_page(call.message.chat.id, page_ind, image_ind, True, lowprice_data, 'lowprice_page', 'lowprice_image')
    else:
        bot.send_message(chat_id=call.message.chat.id, text="Нет отелей для просмотра")


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page')
def hotel_page_callback(call):
    page_ind = int(call.data.split('#')[1])
    if not(page_ind == lowprice_data[call.message.chat.id].cur_page_index):
        image_ind = 1
        change_hotel_page(call.message.chat.id, page_ind, image_ind, False, lowprice_data, 'lowprice_page', 'lowprice_image')


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_image')
def hotel_image_callback(call):
    hotel_image_slide_photo(call, lowprice_data, 'lowprice_page', 'lowprice_image')





