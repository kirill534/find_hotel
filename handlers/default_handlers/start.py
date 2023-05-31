from loguru import logger
from telebot.types import Message

import database
import keyboards
from loader import bot
from states.user_states import UserInputState


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Запуск бота и создание параметров
    :param message: Message
    :return: None
    """
    logger.info(
        "Пользователь ввел команду "
        + message.text
        + f"(id user - {message.from_user.id})"
    )
    bot.delete_message(message.chat.id, message.message_id)
    bot.set_state(message.chat.id, None)
    with bot.retrieve_data(message.chat.id) as data:
        if not data:
            data['query_counter'] = 0
            data["quantity_children"] = 1
            data["age_children"] = [{"age": 5},]
            data["adults"] = 2
            data["old_currencies"] = "usd"
            data["currencies"] = "usd"
            data["currencies_sign"] = "$"
            data["save_info"] = "Нет"
            data['user_id'] = message.from_user.id
        data["flag_checking"] = False

    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.full_name}!"
        f" Я рад, что ты решился воспользоваться моим ботом."
        f" Перед началом использования рекомендую прочитать описание бота в разделе 'Помощь' /menu.",
    )

    database.add_to_db.add_user(message)
