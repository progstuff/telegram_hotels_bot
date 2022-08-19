from loader import bot
from handlers.custom_handlers.lowprice import lowprice_data
from states.lowprice_information import UserLowPriceState
from keyboards.inline.yes_no import get_yes_no_keyboard
from keyboards.inline.hotels_chooser import get_hotels_numbers_choose_keyboard
from utils.misc.hotel_utils import change_hotel_page, hotel_image_slide_photo
from db.hotels_parser import get_lowprice_data_from_server, get_images_links_from_server


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_hotel_pages_number')
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
    if call.data.split('#')[1] == 'yes':
        lowprice_data[call.message.chat.id].image_choose = True

        keyboard = get_hotels_numbers_choose_keyboard('lowprice_image_pages_number', [1, 2, 3])
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Шаг 3 из 3: выберите сколько фото показывать для каждого отеля',
                              reply_markup=keyboard)
        bot.set_state(call.message.from_user.id, UserLowPriceState.max_images_cnt, call.message.chat.id)
    else:
        lowprice_data[call.message.chat.id].image_choose = False
        mes = get_info_message(lowprice_data, call.message.chat.id)
        bot.send_message(chat_id=call.message.chat.id, text=mes)
        bot.delete_state(call.message.from_user.id, call.message.chat.id)
        load_data(call.message.chat.id, lowprice_data)
        

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_image_pages_number')
def hotels_show_image_choose(call):
    max_images_cnt = int(call.data.split('#')[1])
    lowprice_data[call.message.chat.id].max_image_index = max_images_cnt

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text='Вы выбрали показывать по {0} фото для отеля'.format(max_images_cnt))

    mes = get_info_message(lowprice_data, call.message.chat.id)
    bot.send_message(chat_id=call.message.chat.id, text=mes)
    bot.delete_state(call.message.from_user.id, call.message.chat.id)
    load_data(call.message.chat.id, lowprice_data)

@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_page')
def hotel_page_callback(call):
    page_ind = int(call.data.split('#')[1])
    if not(page_ind == lowprice_data[call.message.chat.id].cur_page_index):
        image_ind = 1
        change_hotel_page(call.message.chat.id, page_ind, image_ind, False, lowprice_data, 'lowprice_page', 'lowprice_image')


@bot.callback_query_handler(func=lambda call: call.data.split('#')[0]=='lowprice_image')
def hotel_image_callback(call):
    hotel_image_slide_photo(call, lowprice_data, 'lowprice_page', 'lowprice_image')


def get_info_message(data_storage, chat_id):
    pages_cnt = data_storage[chat_id].max_page_index
    city = data_storage[chat_id].city
    if data_storage[chat_id].image_choose:
        max_images_cnt = data_storage[chat_id].max_image_index
        mes = """Все данные получены. Выбраны следующие параметры запроса:\n
            \tгород: {0}
            \tколичество отелей в выдаче: {1}
            \tколичество фото для отеля: {2}\n\nНачинаю загрузку отелей""".format(city, pages_cnt, max_images_cnt)
    else:
        mes = """Все данные получены. Выбраны следующие параметры запроса:\n
                    \tгород: {0}
                    \tколичество отелей в выдаче: {1}
                    \tне показывать фото отелей\n\nНачинаю загрузку отелей""".format(city, pages_cnt)
    return mes


def load_data(chat_id, data_storage):
    hotels_cnt = get_lowprice_data_from_server(chat_id)
    if hotels_cnt > 0:
        if hotels_cnt < lowprice_data[chat_id].max_page_index:
            lowprice_data[chat_id].max_page_index = hotels_cnt
            bot.send_message(chat_id=chat_id, text="Доступно отелей для просмотра: {}".format(hotels_cnt))
            image_choose = data_storage[chat_id].image_choose
            if image_choose:
                max_images_cnt = data_storage[chat_id].max_image_index
                get_images_links_from_server(chat_id, max_images_cnt)

        page_ind = 1
        image_ind = 1
        change_hotel_page(chat_id, page_ind, image_ind, True, lowprice_data, 'lowprice_page', 'lowprice_image')
    else:
        bot.send_message(chat_id=chat_id, text="Нет отелей для просмотра")
