import json
from typing import Dict


def get_city(response_text: str) -> Dict:
    """
    Функция для извлечения информации о городах из текстового ответа API.
    :param response_text: текстовый ответ API.
    :return: словарь с информацией о возможных городах, где ключ - идентификатор города,
    значение - словарь с информацией о городе, включая его идентификатор и название региона.
    """
    possible_cities = {}
    data = json.loads(response_text)

    if not data:
        raise LookupError('Запрос пуст...')
    for id_place in data['sr']:
        try:
            possible_cities[id_place['gaiaId']] = {
                "gaiaId": id_place['gaiaId'],
                "regionNames": id_place['regionNames']['fullName']
            }
        except KeyError:
            continue
    return possible_cities


def hotel_info(hotels_request: str) -> Dict:
    """
    Функция "hotel_info" принимает в качестве аргумента строку "hotels_request",
    содержащую данные в формате JSON о гостинице.
    Функция возвращает словарь с информацией о гостинице, извлеченной из переданного JSON.
    :param hotels_request: строка с данными о гостинице в формате JSON
    :return: словарь с информацией о гостинице
    """
    data = json.loads(hotels_request)

    if not data:
        raise LookupError('Запрос пуст...')
    hotel_data = {
        'id': data['data']['propertyInfo']['summary']['id'], 'name': data['data']['propertyInfo']['summary']['name'],
        'address': data['data']['propertyInfo']['summary']['location']['address']['addressLine'],
        'coordinates': data['data']['propertyInfo']['summary']['location']['coordinates'],
        'review': data['data']['propertyInfo']['reviewInfo']['summary']['overallScoreWithDescriptionA11y']['value'],
        'description': data['data']['propertyInfo']['summary']['tagline'],
        'images': [
            url['image']['url'] for url in data['data']['propertyInfo']['propertyGallery']['images']

        ]
    }

    return hotel_data


def get_hotels(
        response_text: str,
        command: str,
        landmark_in: str,
        landmark_out: str,
        price_min: str,
        price_max: str) -> Dict:
    """
    Принимает ответ от сервера, выбранную команду сортировки, а так же пределы диапазона
    расстояния от центра города. Возвращает отсортированный словарь, в зависимости от команды сортировки.
    :param response_text: str Ответ от сервера, в котором содержится информация об отелях
    :param command: str Команда сортировки
    :param landmark_in: str Начало диапазона расстояния до центра
    :param landmark_out: str Конец диапазона расстояния до центра
    :param price_min: str Минимальная цена
    :param price_max: str Максимальная цена
    :return: Dict Возвращает словарь с данными об отелях
    """
    data = json.loads(response_text)

    if not data:
        raise LookupError("Запрос пуст...")
    if "errors" in data.keys():
        return {"error": data["errors"][0]["message"]}

    hotels_data = {}
    for hotel in data["data"]["propertySearch"]["properties"]:
        try:
            hotels_data[hotel["id"]] = {
                "name": hotel["name"],
                "id": hotel["id"],
                "distance": hotel["destinationInfo"]["distanceFromDestination"]["value"],
                "unit": hotel["destinationInfo"]["distanceFromDestination"]["unit"],
                "price": hotel["price"]["lead"]["amount"],
            }
        except (KeyError, TypeError):
            continue

    if command == "lowprice":
        hotels_data = {
            key: value
            for key, value in sorted(
                hotels_data.items(),
                key=lambda hotel_id: hotel_id[1]["price"]
                if hotel_id[1]["price"] > 0
                else float("inf"),
            )
        }

    elif command == "highprice":
        hotels_data = {
            key: value
            for key, value in sorted(
                hotels_data.items(),
                key=lambda hotel_id: hotel_id[1]["price"]
                if hotel_id[1]["price"] > 0
                else float("inf"),
                reverse=True,
            )
        }

    elif command == "bestdeal":
        hotels_data = {}
        for hotel in data["data"]["propertySearch"]["properties"]:
            if (
                    float(landmark_in)
                    < hotel["destinationInfo"]["distanceFromDestination"]["value"]
                    < float(landmark_out)
            ):
                if (
                        float(price_min)
                        < hotel["price"]["lead"]["amount"]
                        < float(price_max)
                ):
                    hotels_data[hotel["id"]] = {
                        "name": hotel["name"],
                        "id": hotel["id"],
                        "distance": hotel["destinationInfo"]["distanceFromDestination"]["value"],
                        "unit": hotel["destinationInfo"]["distanceFromDestination"]["unit"],
                        "price": hotel["price"]["lead"]["amount"],
                    }
        hotels_data = {
            key: value
            for key, value in sorted(
                hotels_data.items(),
                key=lambda hotel_id: hotel_id[1]["distance"]
                if hotel_id[1]["price"] > 0
                else float("inf"),
            )
        }

    return hotels_data
