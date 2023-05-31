from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message


def show_buttons_currencies(message: Message, data: dict) -> None:

    """
    Вызов в чат инлайн-кнопок с выбором валюты
    :param message : Message
    :param data: Dict словарь, с возможными вариантами городов
    :return : None
    """
    logger.info("Вывод кнопок с выбором валюты. ")
    keyboard_currencie = types.InlineKeyboardMarkup()
    keyboard_currencie.add(types.InlineKeyboardButton(text="🇧🇾BYN🇧🇾", callback_data="byn"))
    keyboard_currencie.add(types.InlineKeyboardButton(text="🇷🇺RUB🇷🇺", callback_data="rub"))
    keyboard_currencie.add(types.InlineKeyboardButton(text="🇺🇸USD🇺🇸", callback_data="usd"))
    if not data['flag_checking']:
        keyboard_currencie.row(types.InlineKeyboardButton(text="Выход", callback_data="exit"))
    bot.send_message(
        message.chat.id,
        text="Выберите валюту в которой будет выводится стоимость проживания",
        reply_markup=keyboard_currencie,
    )


