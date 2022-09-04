from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_distance_choose_keyboard(key_data: str, dist_vals: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for ind, distance in enumerate(dist_vals):
        if distance == -1:
            button_text = 'не имеет значения'
        else:
            button_text = 'до {} км'.format(distance)
        keyboard.add(InlineKeyboardButton(text=button_text,
                                          callback_data='{0}#{1}#{2}'.format(key_data, 0, button_text)))
    return keyboard


