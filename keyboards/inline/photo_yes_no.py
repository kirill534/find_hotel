from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message
from states.user_states import UserInputState


def show_buttons_photo(message: Message) -> None:
    """
    Вызов в чат инлайн-кнопок с вопросом - нужны ли пользователю фотографии?
    : param message : Message
    : return : None
    """

    logger.info("Вывод кнопок о необходимости фотографий пользователю.")
    keyboard_yes_no = types.InlineKeyboardMarkup()
    keyboard_yes_no.add(types.InlineKeyboardButton(text="ДА", callback_data="да"))
    keyboard_yes_no.add(types.InlineKeyboardButton(text="НЕТ", callback_data="нет"))
    keyboard_yes_no.row(types.InlineKeyboardButton(text="Выход", callback_data="exit"))

    bot.set_state(message.chat.id, state=UserInputState.photo_need)
    bot.send_message(
        message.chat.id, text="Нужно вывести фотографии?", reply_markup=keyboard_yes_no
    )
