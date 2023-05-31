from loader import bot
from telebot import types


def buttons_exit(message: types.Message, text: str) -> None:
    """
    Вызов в чат инлайн-кнопку с выходом
    :param message: Message
    :param text: str
    :return: None
    """

    keyboards_exit = types.InlineKeyboardMarkup()
    keyboards_exit.row(types.InlineKeyboardButton(text="Выход", callback_data="exit"))

    bot.send_message(
        message.chat.id, text=text,
        reply_markup=keyboards_exit, parse_mode="HTML",
    )
