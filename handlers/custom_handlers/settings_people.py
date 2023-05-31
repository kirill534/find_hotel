import re
import keyboards
from loader import bot
from telebot import types
from loguru import logger
from states.user_states import UserInputState


@bot.message_handler(state=UserInputState.adults)
def input_quantity_adults(message: types.Message) -> None:
    """
    Ввод количества взрослых человек, а так же проверка, является ли
    введённое числом и входит ли оно в заданный диапазон от 1 до 3
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 3:
            logger.info(
                "Пользователь ввёл количество взрослых человек: "
                + message.text
                + f"(id user - {message.from_user.id})"
            )
            with bot.retrieve_data(message.chat.id) as data:
                data["adults"] = int(message.text)
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
            bot.set_state(message.chat.id, UserInputState.quantity_children)
            bot.send_message(
                message.chat.id,
                text=f"Введите количество детей (от 0 до 3):",
            )
        else:
            bot.send_message(
                message.chat.id,
                text='Ошибка! Это должно быть число в диапазоне от 1 до 3! Повторите ввод!'
            )
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


@bot.message_handler(state=UserInputState.quantity_children)
def input_quantity_adults(message: types.Message) -> None:
    """
    Ввод количества детей, а так же проверка, является ли
    введённое числом и входит ли оно в заданный диапазон от 1 до 3
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        if 0 <= int(message.text) <= 3:
            logger.info(
                "Пользователь ввёл количество детей: "
                + message.text
                + f"(id user - {message.from_user.id})"
            )
            with bot.retrieve_data(message.chat.id) as data:
                data["quantity_children"] = message.text
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)

            if int(data["quantity_children"]) == 0:
                bot.send_message(
                    message.chat.id,
                    f'Изменение успешное. Взрослых: {data["adults"]}. Детей: {data["quantity_children"]}',
                )
                bot.set_state(message.chat.id, None)
                if data['flag_checking']:
                    keyboards.inline.check_info.buttons_info(message, data)
                else:
                    keyboards.inline.settings_buttons.show_buttons_settings(message, data)
            else:
                bot.set_state(message.chat.id, UserInputState.age_children)
                bot.send_message(
                    message.chat.id,
                    text=f"Введите возраст(от 1 до 17), если несколько детей, вводите через возраст через пробел\n"
                    f"Пример: 12 7",
                )
        else:
            bot.send_message(
                message.chat.id,
                text='Ошибка! Это должно быть число в диапазоне от 0 до 3! Повторите ввод!'
            )
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


@bot.message_handler(state=UserInputState.age_children)
def input_quantity_adults(message: types.Message) -> None:
    """
    Ввод возраста детей, а так же проверка, на количество детей
    и проверка на возраст детей от 1 до 17
    :param message : Message
    :return : None
    """
    logger.info(
        "Пользователь ввёл возраст детей: "
        + message.text
        + f"(id user - {message.from_user.id})"
    )
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    with bot.retrieve_data(message.chat.id) as data:
        try:
            digits = list(map(int, message.text.split()))
            if len(digits) == int(data["quantity_children"]):
                if not any(i > 17 for i in digits):
                    if not any(i < 1 for i in digits):
                        data["age_children"] = [{"age": int(age)} for age in digits]
                        bot.send_message(
                            message.chat.id,
                            f'Изменение успешное. Взрослых: {data["adults"]}. Детей: {data["quantity_children"]}',
                        )
                        bot.set_state(message.chat.id, None)
                        if data['flag_checking']:
                            keyboards.inline.check_info.buttons_info(message, data)
                        else:
                            keyboards.inline.settings_buttons.show_buttons_settings(message, data)
                    else:
                        bot.send_message(
                            message.chat.id,
                            text="Ошибка! Вы ввели возраст ребенка меньше 1",
                        )
                else:
                    bot.send_message(
                        message.chat.id,
                        text="Ошибка! Вы ввели возраст ребенка больше 17",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    text=f"Ошибка! Вы ввели меньше/больше возрастов, чем количество детей ({data['quantity_children']})"
                )
        except ValueError:
            bot.send_message(
                message.chat.id,
                text=f"Ошибка! Вы ввели кроме цифр что-то ещё! Повторите ввод!"
            )
