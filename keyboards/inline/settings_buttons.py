from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message


def show_buttons_settings(message: Message, data: dict) -> None:
    """
    Вызов в чат инлайн-кнопок c изменениями
    :param message : Message
    :param data: Dict словарь, с возможными вариантами городов
    :return : None
    """
    logger.info("Вывод кнопок с выбором изменений. ")
    keyboard_currencie = types.InlineKeyboardMarkup()
    keyboard_currencie.add(
        types.InlineKeyboardButton(text="💰 Изменить валюту", callback_data="currency")
    )
    keyboard_currencie.add(
        types.InlineKeyboardButton(
            text="👨‍👩‍👦 Изменить количество человек", callback_data="quantity_people"
        )
    )
    if not data["flag_checking"]:
        keyboard_currencie.row(
            types.InlineKeyboardButton(text="Выход", callback_data="exit")
        )
    bot.send_message(
        message.chat.id,
        text="Выберите интересующее изменение",
        reply_markup=keyboard_currencie,
    )
