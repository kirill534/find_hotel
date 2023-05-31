import database
import keyboards.inline.menu_buttuns
from loader import bot
from telebot import types
from loguru import logger
from states.user_states import UserInputState


def buttons_number(message: types.Message) -> None:
    """
    Вызов в чат reply-кнопки с числами
    : param message : Message
    : return : None
    """
    logger.info(f"Получены записи из таблицы query. User_id: {message.chat.id}")
    queries = database.read_from_db.read_query(message.chat.id)

    if queries:
        markup = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
        markup.add(
            *[
                types.InlineKeyboardButton(text=item[1], callback_data=item[1])
                for item in queries
            ]
        )
        bot.set_state(message.chat.id, UserInputState.select_number)
        bot.send_message(
            message.chat.id,
            text="Введите номер интересующего вас варианта: ",
            reply_markup=markup,
        )

        for item in queries:
            bot.send_message(
                message.chat.id,
                f"({item[1]}). Команда: {item[0]}.\nДата и время: {item[2]}. Вы вводили город: {item[3]}",
            )

    else:
        bot.send_message(message.chat.id, "В базе данных пока нет записей")
        bot.set_state(message.chat.id, None)
        keyboards.inline.menu_buttuns.show_buttons_commands(message)
