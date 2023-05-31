from loguru import logger
from loader import bot
from telebot import types
from telebot.types import Message, Dict


def show_cities_buttons(message: Message, possible_cities: Dict) -> None:
    """
    Функция, из словаря возможных городов,
    формирует инлайн-клавиатуру с вариантами городов, и посылает её в чат.
    :param message: Message
    :param possible_cities: Dict словарь, с возможными вариантами городов
    :return: None
    """
    logger.info("Вывод кнопок с городами")
    keyboards_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboards_cities.add(
            types.InlineKeyboardButton(
                text=value["regionNames"], callback_data=value["gaiaId"]
            )
        )
    keyboards_cities.row(types.InlineKeyboardButton(text="Выход", callback_data="exit"))

    bot.send_message(
        message.from_user.id,
        text="Пожалуйста, выберите город",
        reply_markup=keyboards_cities,
    )