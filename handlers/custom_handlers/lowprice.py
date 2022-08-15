from loader import bot
from telebot.types import Message
from config_data.config import LOW_PRICE_COMMAND
from utils.misc.rapid_api_utils import get_lowprice_hotels
import json


@bot.message_handler(commands=[LOW_PRICE_COMMAND['command_name']])
def lowprice(message: Message) -> None:
    bot.send_message(message.from_user.id, 'вы выбрали показать топ самых дешевых отелей в городе. Введите город')
    is_success, hotels = get_lowprice_hotels('new york')
    if is_success:
        with open('result.json', 'w') as file:
            json.dump(hotels, file, indent=4)
    print(hotels)


@bot.message_handler(content_types='text')
def lowprice_button_message(message: Message) -> None:
    if message.text == LOW_PRICE_COMMAND['command_description']:
        lowprice(message)


