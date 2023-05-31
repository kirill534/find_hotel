import keyboards
from loguru import logger
from telebot.types import CallbackQuery
from loader import bot
from states.user_states import UserInputState


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def destination_id_callback(call: CallbackQuery) -> None:
    if int(call.data) > 100:
        logger.info('Запись id города: ' + call.data)

        bot.set_state(call.message.chat.id, UserInputState.destinationId)
        with bot.retrieve_data(call.message.chat.id) as data:
            data['destination_id'] = call.data
            if data['info_cities'][call.data]['gaiaId'] == call.data:
                data['city'] = data['info_cities'][call.data]['regionNames']
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if data['flag_checking']:
            keyboards.inline.check_info.buttons_info(call.message, data)
        else:
            keyboards.inline.number_buttons.buttons_number(call.message)
    else:
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
