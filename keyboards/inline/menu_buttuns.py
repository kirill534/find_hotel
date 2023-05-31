from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot
from telebot import types
from loguru import logger


def show_buttons_commands(message: types.Message) -> None:
    """
    Вызов в чат инлайн-кнопок со всеми встроенными командами
    : param message : Message
    : return : None
    """

    logger.info("Вывод начальных кнопок с командами")
    lowprice_button = InlineKeyboardButton(text="↘ Дешевые", callback_data="lowprice")
    highprice_button = InlineKeyboardButton(text="↗ Дорогие", callback_data="highprice")
    bestdeal_button = InlineKeyboardButton(text="✅ С ценой", callback_data="bestdeal")

    settings_button = InlineKeyboardButton(text="⚙ Настройки", callback_data="settings")
    history_button = InlineKeyboardButton(text="📚 История", callback_data="history")
    help_button = InlineKeyboardButton(text="🆘 Помощь", callback_data="help")

    button_row = (
        InlineKeyboardMarkup()
        .row(lowprice_button, highprice_button, bestdeal_button)
        .row(settings_button, history_button, help_button)
    )

    bot.send_message(message.chat.id, text="Выберите команду", reply_markup=button_row)
