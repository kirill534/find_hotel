import handlers
import keyboards.inline.number_buttons
import parser
import utils
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from telebot.types import Dict
from loader import bot
from loguru import logger
from telebot.types import CallbackQuery
from states.user_states import UserInputState


def buttons_info(message: types.Message, data: Dict) -> None:
    """
    Вызов в чат инлайн-кнопок с проверкой введенных параметров
    : param message : Message
    : return : None
    """
    global button_row

    logger.info('Вывод кнопок с проверкой всей информации')
    data['flag_checking'] = True

    city_button = InlineKeyboardButton(
        text=f'🌇 Город: {data["city"]}', callback_data="city"
    )
    data_button = InlineKeyboardButton(
        text=f'📅 Временной интервал {data["checkInDate"]["day"]}-'
             f'{data["checkInDate"]["month"]}-{data["checkInDate"]["year"]} / {data["checkOutDate"]["day"]}-'
             f'{data["checkOutDate"]["month"]}-{data["checkOutDate"]["year"]}',
        callback_data="interval_data",
    )
    quantity_hotel_button = InlineKeyboardButton(
        text=f'🏨 Отелей: {data["quantity_hotels"]}', callback_data="qntt_htl"
    )
    need_photo = InlineKeyboardButton(
        text=f'📷 Фото: {data["photo_need"]}', callback_data="pht_nd"
    )
    quantity_photo_button = InlineKeyboardButton(
        text=f'Кол-во фото: {data["photo_count"]}', callback_data="qntt_pht"
    )
    settings_button = InlineKeyboardButton(
        text=f'💰 Валюта: {data["currencies_sign"]}'
             f' {"🧑🏼" * int(data["adults"])} взрослых. {"👶🏼" * int(data["quantity_children"])} детей',
        callback_data="sttngs"
    )
    save_button = InlineKeyboardButton(
        text=f'💾 Сохранить: {data["save_info"]}', callback_data="save"
    )
    continue_button = InlineKeyboardButton(text="🔎 Найти", callback_data="continue")

    if data["command_buttons"].startswith("bestdeal"):
        price_hotel = InlineKeyboardButton(
            text=f"💰 Ценовой диапазон: "
                 f'{currency_transfer(data, data["price_min"])} - '
                 f'{currency_transfer(data, data["price_max"])} '
                 f'{data["currencies_sign"]}',
            callback_data="prc_htl",
        )
        distance_to_center = InlineKeyboardButton(
            text=f'🚕 Расстояние до центра: {round(data["landmark_in"] * 1.6093, 2)} - '
                 f'{round(data["landmark_out"] * 1.6093, 2)} км',
            callback_data="distance",
        )

        if data["photo_need"] == "да":
            button_row = (
                InlineKeyboardMarkup()
                .add(city_button)
                .add(data_button)
                .row(quantity_hotel_button, need_photo, quantity_photo_button)
                .add(price_hotel)
                .add(distance_to_center)
                .add(settings_button)
                .add(save_button)
                .add(continue_button)
            )
        else:
            button_row = (
                InlineKeyboardMarkup()
                .add(city_button)
                .add(data_button)
                .row(quantity_hotel_button, need_photo)
                .add(price_hotel)
                .add(distance_to_center)
                .add(settings_button)
                .add(save_button)
                .add(continue_button)
            )

    elif data["command_buttons"].startswith(("lowprice", "highprice")):
        if data["photo_need"] == "да":
            button_row = (
                InlineKeyboardMarkup()
                .add(city_button)
                .add(data_button)
                .row(quantity_hotel_button, need_photo, quantity_photo_button)
                .add(settings_button)
                .add(save_button)
                .add(continue_button)
            )
        else:
            button_row = (
                InlineKeyboardMarkup()
                .add(city_button)
                .add(data_button)
                .row(quantity_hotel_button, need_photo)
                .add(settings_button)
                .add(save_button)
                .add(continue_button)
            )

    bot.send_message(message.chat.id, text=f"Текущий запрос - {data['command_buttons']}. Всё верно?",
                     reply_markup=button_row)


@bot.callback_query_handler(func=lambda call: call.data.startswith(('city', 'interval_data', 'qntt_htl', 'pht_nd',
                                                                    'qntt_pht', 'prc_htl', 'distance', 'sttngs', 'save',
                                                                    'continue')))
def commands_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку 'city'/'interval_data'/'qntt_htl'/'pht_nd',/
                                'qntt_pht'/'prc_htl'/'distance'/'sttngs'/'continue'

    : param call: 'city'/'interval_data'/'qntt_htl'/'pht_nd',/
    'qntt_pht'/'prc_htl'/'distance'/'sttngs'/,'save'/'continue'
    : return : None
    """

    logger.info('Нажата кнопка для изменения: ' + call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data == "qntt_htl":
            keyboards.inline.number_buttons.buttons_number(call.message)

        elif call.data == "city":
            bot.set_state(call.message.chat.id, UserInputState.input_city)
            bot.send_message(
                call.message.chat.id, text="Введите город в котором нужно найти отель: "
            )

        elif call.data == "interval_data":
            del data["checkInDate"]
            handlers.custom_handlers.user_commands.my_calendar(call.message, "заезда")

        elif call.data == "pht_nd":
            data["photo_need"] = "нет" if data["photo_need"] == "да" else "да"
            if data["photo_need"] == "да":
                data["photo_count"] = 1
            else:
                data["photo_count"] = 0
            keyboards.inline.check_info.buttons_info(call.message, data)

        elif call.data == "qntt_pht":
            bot.set_state(call.message.chat.id, UserInputState.photo_count)
            bot.send_message(
                call.message.chat.id, text="Сколько вывести фотографий? От 1 до 10!"
            )

        elif call.data == "prc_htl":
            data["old_currencies"] = data["currencies"]
            bot.set_state(call.message.chat.id, UserInputState.priceMin)
            bot.send_message(
                call.message.chat.id,
                text=f'Введите минимальную стоимость отеля в {data["currencies_sign"]}.',
            )

        elif call.data == "distance":
            bot.set_state(call.message.chat.id, UserInputState.landmarkIn)
            bot.send_message(
                call.message.chat.id,
                text="Введите начало диапазона расстояния от центра (от 0 км).",
            )

        elif call.data == "sttngs":
            keyboards.inline.settings_buttons.show_buttons_settings(
                call.message, data
            )

        elif call.data == "save":
            data["save_info"] = "Нет" if data["save_info"] == "Да" else "Да"
            keyboards.inline.check_info.buttons_info(call.message, data)

        elif call.data == "continue":
            data["flag_checking"] = False
            bot.send_message(call.message.chat.id, text="Идёт поиск подходящих отелей.....")
            utils.find_hotel.find_and_show_hotels(call.message, data)

        else:
            bot.send_message(
                call.message.chat.id, text="Ошибка! Нажмите на кнопку"
            )


def currency_transfer(data, price) -> float:
    """
    Функция проверяющая валюту, если валюта разная переводит в нужную
    :param data: Dict данные, собранные от пользователя
    :param price: float цена
    :return: float новая цена
    """
    if data["old_currencies"] == data["currencies"]:
        return price
    return round(
        parser.conventer.convert_currency_xe(
            data["old_currencies"].upper(), data["currencies"].upper(), price), 2,
    )
