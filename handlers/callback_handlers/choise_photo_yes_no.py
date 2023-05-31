from handlers.custom_handlers.user_commands import my_calendar
from loader import bot
from loguru import logger
from telebot.types import CallbackQuery
from states.user_states import UserInputState


@bot.callback_query_handler(func=lambda call: call.data.startswith(('да', 'нет')))
def need_photo_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку "ДА" или "НЕТ"
    :param call: "да" or "нет"
    :return : None
    """
    logger.info('Нажата кнопка: ' + call.data)
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data == 'да':
            data['photo_need'] = call.data
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.set_state(call.message.chat.id, UserInputState.photo_count)
            bot.send_message(call.message.chat.id, 'Сколько вывести фотографий? От 1 до 10!')
        elif call.data == 'нет':
            data['photo_need'] = call.data
            data['photo_count'] = '0'
            bot.delete_message(call.message.chat.id, call.message.message_id)
            my_calendar(call.message, 'заезда')