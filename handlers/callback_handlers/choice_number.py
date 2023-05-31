import keyboards
from loguru import logger
from telebot.types import CallbackQuery
from loader import bot


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def number_callback(call: CallbackQuery) -> None:
    if 0 < int(call.data) <= 15:
        logger.info(
            f'Пользователь выбрал кол-во отелей: ' + call.data + f' id user - ({call.message.from_user.id})'
        )
        with bot.retrieve_data(call.message.chat.id) as data:
            data['quantity_hotels'] = call.data
            if data['flag_checking']:
                bot.set_state(call.message.chat.id, None)
                bot.delete_message(call.message.chat.id, call.message.message_id)
                keyboards.inline.check_info.buttons_info(call.message, data)
            else:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                keyboards.inline.photo_yes_no.show_buttons_photo(call.message)
    else:
        bot.send_message(
            call.message.chat.id,
            text='Ошибка! Это должно быть число в диапазоне от 1 до 15! Повторите ввод!'
        )