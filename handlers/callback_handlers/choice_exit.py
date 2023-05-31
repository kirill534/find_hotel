from loguru import logger
from telebot.types import CallbackQuery
import keyboards.inline.menu_buttuns
from loader import bot


@bot.callback_query_handler(func=lambda call: call.data.startswith('exit'))
def destination_id_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку выхода
    :param call: "exit"
    :return: None
    """
    if call.data:
        bot.set_state(call.message.chat.id, None)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        logger.info('Нажата кнопка: ' + call.data + f' ({call.message.from_user.id})')
        keyboards.inline.menu_buttuns.show_buttons_commands(call.message)