import keyboards
from loguru import logger
from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["menu"])
def bot_start(message: Message) -> None:
    """
    Функция добавляет в словарь нужные параметры и вызывает
    inline-клавиатуру со всеми командами.
    :param message: Message
    :return: None
    """
    logger.info(
        "Пользователь ввел команду "
        + message.text
        + f"(id user - {message.from_user.id})"
    )
    bot.set_state(message.chat.id, None)
    with bot.retrieve_data(message.chat.id) as data:
        data["flag_checking"] = False
    keyboards.inline.menu_buttuns.show_buttons_commands(message)

