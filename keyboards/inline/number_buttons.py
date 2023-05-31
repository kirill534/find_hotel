from loader import bot
from telebot import types
from loguru import logger
from states.user_states import UserInputState


def buttons_number(message: types.Message) -> None:
    """
    Вызов в чат инлайн-кнопку с числами от 1 до 15
    : param message : Message
    : return : None
    """
    logger.info("Вывод кнопок c числами от 1 до 15")
    keyboards_number = types.InlineKeyboardMarkup(row_width=5)
    keyboards_number.add(
        *[
            types.InlineKeyboardButton(text=number, callback_data=number)
            for number in range(1, 6)
        ]
    )
    keyboards_number.add(
        *[
            types.InlineKeyboardButton(text=number, callback_data=number)
            for number in range(6, 11)
        ]
    )
    keyboards_number.add(
        *[
            types.InlineKeyboardButton(text=number, callback_data=number)
            for number in range(11, 16)
        ]
    )
    keyboards_number.row(types.InlineKeyboardButton(text="Выход", callback_data="exit"))

    bot.set_state(message.chat.id, state=UserInputState.quantity_hotels)
    bot.send_message(
        message.chat.id,
        text="Сколько вывести отелей в чат? Не более 15!",
        reply_markup=keyboards_number,
    )
