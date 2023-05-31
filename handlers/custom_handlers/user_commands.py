import api_choice.general_request
import keyboards.inline.city_buttons
import utils
from telebot import types
from keyboards.inline.calendar_buttons import Calendar
from loader import bot
from states.user_states import UserInputState
from loguru import logger


@bot.message_handler(state=UserInputState.input_city)
def input_city(message: types.Message) -> None:
    """
    Ввод пользователем города и отправка запроса серверу на поиск вариантов городов.
    Возможные варианты городов передаются генератору клавиатуры.
    :param message : Message
    :return : None
    """
    with bot.retrieve_data(message.chat.id) as data:
        logger.info(
            "Пользователь ввёл город: "
            + message.text
            + f"(id user - {message.from_user.id})"
        )

        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": message.text, "locale": "ru_RU"}
        response_cities = api_choice.general_request.request(
            "GET", url, querystring
        )
        if response_cities.status_code == 200:
            possible_cities = utils.processing_json.get_city(
                response_cities.text
            )
            data['info_cities'] = possible_cities
            keyboards.inline.city_buttons.show_cities_buttons(
                message, possible_cities
            )
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        else:
            bot.send_message(
                message.chat.id,
                text="Что-то пошло не так!\n" "Попробуйте ввести другой город",
            )


@bot.message_handler(state=UserInputState.quantity_hotels)
def input_quantity_hotel(message: types.Message):
    """
    Ввод количества выдаваемых на странице отелей, а так же проверка, является ли
    введённое числом и входит ли оно в заданный диапазон от 1 до 15
    :param message : Message
    :return : None
    """
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    if message.text.isdigit():
        if 0 < int(message.text) <= 15:
            logger.info(
                "Пользователь ввёл кол-во отелей: "
                + message.text
                + f"(id user - {message.from_user.id})"
            )
            with bot.retrieve_data(message.chat.id) as data:
                data["quantity_hotels"] = message.text
                if data["flag_checking"]:
                    keyboards.inline.check_info.buttons_info(message, data)
                else:
                    keyboards.inline.photo_yes_no.show_buttons_photo(message)
        else:
            bot.send_message(
                message.chat.id,
                text="Ошибка! Это должно быть число в диапазоне от 1 до 15! Повторите ввод!",
            )
            keyboards.inline.number_buttons.buttons_number(message)
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )
        keyboards.inline.number_buttons.buttons_number(message)


@bot.message_handler(state=UserInputState.photo_need)
def input_quantity_photo(message: types.Message):
    """
    Ввод в необходимости фотографий и проверка на строку и на значения да/нет.
    :param message : Message
    :return : None
    """
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    if message.text.isalpha():
        if message.text == "да":
            logger.info(
                "Пользователь ввёл: "
                + message.text
                + f"(id user - {message.from_user.id})"
            )
            with bot.retrieve_data(message.chat.id) as data:
                data["photo_need"] = message.text
            bot.set_state(message.chat.id, UserInputState.photo_count)
            bot.send_message(
                message.chat.id, text="Сколько вывести фотографий? От 1 до 10!"
            )
        elif message.text == "нет":
            with bot.retrieve_data(message.chat.id) as data:
                data["photo_need"] = message.text
                data["photo_count"] = 0
            my_calendar(message, "заезда")
        else:
            bot.send_message(
                message.chat.id,
                text="Ошибка! Это должно быть да или нет! Повторите ввод!",
            )
            keyboards.inline.photo_yes_no.show_buttons_photo(message)
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не строку! Повторите ввод!"
        )
        keyboards.inline.photo_yes_no.show_buttons_photo(message)


@bot.message_handler(state=UserInputState.photo_count)
def input_photo_quantity(message: types.Message) -> None:
    """
    Ввод количества фотографий и проверка на число и на соответствие заданному диапазону от 1 до 10
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            logger.info(
                "Пользователь ввел количества фотографий: "
                + message.text
                + f"(id user - {message.from_user.id})"
            )
            with bot.retrieve_data(message.chat.id) as data:
                data["photo_count"] = message.text
            if data["flag_checking"]:
                keyboards.inline.check_info.buttons_info(message, data)
            else:
                my_calendar(message, "заезда")
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
        else:
            bot.send_message(
                message.chat.id,
                text="Число фотографий должно быть в диапазоне от 1 до 10! Повторите ввод!",
            )
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


@bot.message_handler(state=UserInputState.priceMin)
def input_price_min(message: types.Message) -> None:
    """
    Ввод минимальной стоимости отеля и проверка чтобы это было число.
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        logger.info(
            "Пользователь ввёл минимальную стоимость отеля: "
            + message.text
            + f"(id user - {message.from_user.id})"
        )
        with bot.retrieve_data(message.chat.id) as data:
            data["old_currencies"] = data["currencies"]
            data["price_min"] = message.text
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.set_state(message.chat.id, UserInputState.priceMax)
        bot.send_message(
            message.chat.id,
            text=f'Введите максимальную стоимость отеля в {data["currencies_sign"]}:',
        )
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


@bot.message_handler(state=UserInputState.priceMax)
def input_price_max(message: types.Message) -> None:
    """
    Ввод максимальной стоимости отеля и проверка чтобы это было число. Максимальное число не может
    быть меньше минимального.
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        logger.info(
            "Пользователь ввёл максимальную стоимости отеля, сравнение с price_min: "
            + message.text
            + f"(id user - {message.from_user.id})"
        )
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        with bot.retrieve_data(message.chat.id) as data:
            if int(data["price_min"]) < int(message.text):
                data["price_max"] = message.text
                if data["flag_checking"]:
                    keyboards.inline.check_info.buttons_info(message, data)
                else:
                    bot.set_state(message.chat.id, UserInputState.landmarkIn)
                    bot.send_message(
                        message.chat.id,
                        text="Введите начало диапазона расстояния от центра (от 0 метрах).",
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    text="Максимальная цена должна быть больше минимальной. Повторите ввод!",
                )
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


@bot.message_handler(state=UserInputState.landmarkIn)
def input_landmark_in(message: types.Message) -> None:
    """
    Ввод начала диапазона расстояния до центра
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        logger.info(
            "Пользователь ввёл начальное расстояние от центра "
            + message.text
            + f"(id user - {message.from_user.id})"
        )
        with bot.retrieve_data(message.chat.id) as data:
            data["landmark_in"] = int(message.text) * 0.000621
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)
        bot.set_state(message.chat.id, UserInputState.landmarkOut)
        bot.send_message(
            message.chat.id,
            text="Введите конец диапазона расстояния от центра (в метрах).",
        )
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


@bot.message_handler(state=UserInputState.landmarkOut)
def input_landmark_out(message: types.Message) -> None:
    """
    Ввод конца диапазона расстояния до центра
    :param message : Message
    :return : None
    """
    if message.text.isdigit():
        logger.info(
            "Пользователь ввёл конечное расстояние от центра "
            + message.text
            + f"(id user - {message.from_user.id})"
        )
        with bot.retrieve_data(message.chat.id) as data:
            data["landmark_out"] = int(message.text) * 0.000621
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id - 1)
            keyboards.inline.check_info.buttons_info(message, data)
    else:
        bot.send_message(
            message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!"
        )


bot_calendar = Calendar()


def my_calendar(message: types.Message, word: str):
    """
     Запуск инлайн-клавиатуры (календаря) для выбора дат заезда и выезда
     :param message : Message
     :param word : str слово (заезда или выезда)
     :return : None
     """
    bot.send_message(
        message.chat.id,
        f"Выберите дату: {word}",
        reply_markup=bot_calendar.create_calendar(),
    )
