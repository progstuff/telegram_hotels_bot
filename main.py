from telebot.custom_filters import StateFilter

import handlers
from database.command_history_data import initiate_tables
from loader import bot
from utils.set_bot_commands import set_default_commands

if __name__ == '__main__':
    initiate_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()

