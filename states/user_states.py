from telebot.handler_backends import State, StatesGroup


class UserInputState(StatesGroup):
    input_city = State()  # город, который ввел пользователь
    destinationId = State()  # запись id города
    quantity_hotels = State()  # количество отелей, нужное пользователю
    photo_count = State()  # количество фотографий
    input_date = State()  # ввод даты (заезда, выезда)
    priceMin = State()  # минимальная стоимость
    priceMax = State()  # максимальная стоимость
    landmarkIn = State()  # начальное расстояние до центра
    landmarkOut = State()  # конечное расстояние до центра
    command_buttons = State()  # команда
    photo_need = State()  # необходимость фотографий
    select_number = State()  # выбор истории поиска
    adults = State()  # количество взрослых
    quantity_children = State()  # количество детей
    age_children = State()  # возраст детей
