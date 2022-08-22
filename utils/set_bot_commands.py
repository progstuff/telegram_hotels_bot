from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS, CUSTOM_COMMANDS


def set_default_commands(bot) -> None:
    bot.set_my_commands(
        [BotCommand(command['command_name'], command['command_description']) for command in DEFAULT_COMMANDS] +
        [BotCommand(command['command_name'], command['command_description']) for command in CUSTOM_COMMANDS]
    )
