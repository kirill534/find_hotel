import datetime
import json

import database
import keyboards.inline.check_info
import parser.conventer
from loader import bot
from telebot.types import Message, InputMediaPhoto
from loguru import logger
import api_choice
import random
from telebot.types import Dict
from utils.processing_json import get_hotels
from utils.processing_json import hotel_info
from translate import Translator


def find_and_show_hotels(message: Message, data: Dict) -> None:
    """
    Формирование запросов на поиск отелей, и детальной информации о них.
    Вывод полученных данных пользователю в чат.
    : param message : Message
    : param data : Dict данные, собранные от пользователя.
    : return : None
    """
    translator = Translator(from_lang='en', to_lang='ru')

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {"regionId": data['destination_id']},
        "checkInDate": {
            'day': int(data['checkInDate']['day']),
            'month': int(data['checkInDate']['month']),
            'year': int(data['checkInDate']['year'])
        },
        "checkOutDate": {
            'day': int(data['checkOutDate']['day']),
            'month': int(data['checkOutDate']['month']),
            'year': int(data['checkOutDate']['year'])
        },
        "rooms": [
            {
                "adults": data["adults"],
            },
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 30,
    }

    if data["quantity_children"] != 0:
        payload["rooms"][0]["children"] = data["age_children"]

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    response_hotels = api_choice.general_request.request('POST', url, payload)

    logger.info(f'Сервер вернул ответ {response_hotels.status_code}')
    if response_hotels.status_code == 200:

        hotels = get_hotels(response_hotels.text, data['command_buttons'], data["landmark_in"], data["landmark_out"],
                            round(parser.conventer.convert_currency_xe(
                                data['currencies'].upper(), "USD", data['price_min']), 2),
                            round(parser.conventer.convert_currency_xe(
                                data['currencies'].upper(), "USD", data['price_max']), 2))

        if 'error' in hotels or not hotels:
            bot.send_message(message.chat.id, 'Попробуйте осуществить поиск с другими параметрами')
            keyboards.inline.check_info.buttons_info(message, data)
        else:
            count = 0
            data['query_counter'] += 1
            database.add_to_db.add_query(data)
            for hotel in hotels.values():
                if count < int(data['quantity_hotels']):
                    id_sticer = bot.send_sticker(
                        message.chat.id,
                        'CAACAgIAAxkBAAINCWQ21O3-lDWNdgYbBjxLeQkc6ogIAAIZAQACUomRI27pC30cRuNILwQ'
                    )
                    count += 1
                    summary_payload = {
                        "currency": "USD",
                        "eapid": 1,
                        "locale": "en_US",
                        "siteId": 300000001,
                        "propertyId": hotel['id']
                    }
                    summary_url = "https://hotels4.p.rapidapi.com/properties/v2/get-summary"
                    get_summary = api_choice.general_request.request('POST', summary_url, summary_payload)

                    logger.info(f'Сервер вернул ответ {get_summary.status_code}')
                    if get_summary.status_code == 200:

                        summary_info = hotel_info(get_summary.text)
                        number_days_stay = quantity_day(data)

                        ages = ''
                        for c in data["age_children"]:
                            age = c.get('age')
                            if age:
                                ages += f'%3Ac{age}'

                        hotel_link = f"https://www.hotels.com/h{summary_info['id']}.Hotel-Information/" \
                                             f"?chkin={data['checkInDate']['year']}-{data['checkInDate']['month']}" \
                                             f"-{data['checkInDate']['day']}&chkout={data['checkOutDate']['year']}" \
                                             f"-{data['checkOutDate']['month']}-{data['checkOutDate']['day']}" \
                                             f"&rm1=a{data['adults']}{ages}&expediaPropertyId={summary_info['id']}"
                        new_price = round(parser.conventer.convert_currency_xe(
                            "USD", data['currencies'].upper(), hotel["price"]
                        ), 2)

                        info_hotel = f'🛎Название: {hotel["name"]}\n ' \
                                     f'📍Адрес: {summary_info["address"]}\n' \
                                     f'🏆Рейтинг: {summary_info["review"]}\n' \
                                     f'🧾Описание: {translator.translate(summary_info["description"])}\n' \
                                     f'🚕Расстояние до центра: {round(hotel["distance"] * 1.6093, 2)} км.\n' \
                                     f'💴Цена за ночь: ' f'{new_price} {data["currencies_sign"]}\n' \
                                     f'💰Цена за весь период проживания {round(new_price * number_days_stay.days, 2)}' \
                                     f' {data["currencies_sign"]}\n' \
                                     f"🔗Ссылка на отель: {hotel_link}"
                        medias = []
                        links_to_images = []
                        try:
                            for random_url in range(int(data['photo_count'])):
                                links_to_images.append(summary_info['images']
                                                       [random.randint(0, len(summary_info['images']) - 1)])
                        except IndexError:
                            continue

                        data_to_db = {
                            hotel["id"]: {
                                "input_city": data["city"],
                                "name": hotel["name"],
                                "address": summary_info["address"],
                                "user_id": message.chat.id,
                                "price": new_price,
                                "currencies_sign": data["currencies_sign"],
                                "distance": round(hotel["distance"], 2),
                                "date_time": data["date_time"],
                                "images": links_to_images,
                                "hotel_link": hotel_link,
                            }
                        }

                        database.add_to_db.add_response(data_to_db)
                        if int(data['photo_count']) > 0:
                            for number, url in enumerate(links_to_images):
                                if number == 0:
                                    medias.append(InputMediaPhoto(media=url, caption=info_hotel))
                                else:
                                    medias.append(InputMediaPhoto(media=url))

                            logger.info("Выдаю найденную информацию в чат")
                            bot.delete_message(message.chat.id, id_sticer.message_id)
                            bot.send_media_group(message.chat.id, medias)

                        else:
                            logger.info("Выдаю найденную информацию в чат")
                            bot.delete_message(message.chat.id, id_sticer.message_id)
                            bot.send_message(message.chat.id, info_hotel)
                    else:
                        bot.send_message(message.chat.id, f'Что-то пошло не так, код ошибки: {get_summary.status_code}')
                else:
                    break
            bot.send_message(message.chat.id, 'Поиск окончен!')

            if data['save_info'] == 'Нет':
                del data['checkInDate']
            keyboards.inline.menu_buttuns.show_buttons_commands(message)
    else:
        bot.send_message(message.chat.id, f'Что-то пошло не так, код ошибки: {response_hotels.status_code}')


def quantity_day(data: Dict):
    quantity_day_in = f'{data["checkInDate"]["day"]}-{data["checkInDate"]["month"]}-{data["checkInDate"]["year"]}'
    quantity_day_out = f'{data["checkOutDate"]["day"]}-{data["checkOutDate"]["month"]}-{data["checkOutDate"]["year"]}'
    quantity_day_in = quantity_day_in.split('-')
    quantity_day_out = quantity_day_out.split('-')
    day_in = datetime.date(int(quantity_day_in[2]), int(quantity_day_in[1]), int(quantity_day_in[0]))
    day_out = datetime.date(int(quantity_day_out[2]), int(quantity_day_out[1]), int(quantity_day_out[0]))
    number_days_stay = day_out - day_in
    return number_days_stay
