***
# Telegram-бот для поиска отелей

Данный [бот](@diplom534_bot) позволяет подбирать отели с сайта [Hotels.com](https://hotels.com/) в соответствии с Вашими критериями поиска. 
Для разработки и функционирования проекта используется открытый API Hotels,
который расположен на сайте [rapidapi.com](https://rapidapi.com/apidojo/api/hotels4/).

***

## Функционал бота

С помощью данного боты Вы можете:

- подобрать отели по самой низкой или высокой цене;
- подобрать отели по заданному диапазону цены и расстояния от центра города;
- Изменить валюту, а так же количество человек;
- запросить историю запросов.

После введения всех параметров бот позволяет изменить параметры перед тем, как вывести отели.

По каждому отелю бот выводит следующие данные:

- Название отеля;
- Адрес отеля;
- Рейтинг отеля;
- Описание отеля;
- Расстояние до центра в км;
- Цена за ночь;
- Цена за весь период проживания;
- Ссылка на отель.

***

## Описание работы команд

### Команда /start

После ввода команды: 
1. Выводится приветствие пользователю и рекомендует 
прочитать краткое описание по использованию в разделе 'Помощь'.

### Команда /menu

После ввода команды: 
1. Выводятся кнопки всех команд.


### Кнопка Lowprice

После нажатия кнопки у пользователя запрашивается: 
1. Город, где будет проводиться поиск отелей.
2. Выдается список возможных вариантов городов в виде inline-клавиатуры.
3. Выдается список чисел от 1 до 15 в виде inline-клавиатуры, 
с помощью которых пользователь может выбрать количество отелей.
4. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума).
5. Выводится календарь с возможностью выбора даты заезда или выезда. 
6. Выдается список всех введенных параметров с проверкой.

### Кнопка Highprice 

После нажатия кнопки у пользователя запрашивается:
1. Город, где будет проводиться поиск отелей.
2. Выдается список возможных вариантов городов в виде inline-клавиатуры.
3. Выдается список чисел от 1 до 15 в виде inline-клавиатуры, 
с помощью которых пользователь может выбрать количество отелей.
4. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума).
5. Выводится календарь с возможностью выбора даты заезда или выезда. 
6. Выдается список всех введенных параметров с проверкой.

### Кнопка Bestdeal

После нажатия кнопки у пользователя запрашивается:
1. Город, где будет проводиться поиск отелей.
2. Выдается список возможных вариантов городов в виде inline-клавиатуры.
3. Выдается список чисел от 1 до 15 в виде inline-клавиатуры, 
с помощью которых пользователь может выбрать количество отелей.
4. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”). При положительном ответе пользователь также вводит количество необходимых фотографий (не больше заранее определённого максимума).
5. Выводится календарь с возможностью выбора даты заезда или выезда.
6. Запрашиваются минимальная и максимальная стоимость отеля (по умолчанию в доллорах).
7. Диапазон расстояния, на котором находится отель от центра в метрах.
8. Выдается список всех введенных параметров с проверкой.

### Кнопка История

После нажатия кнопки у пользователя выводится история поиска отелей: 
1. Выдает список выполненных пользователем запросом, но не более 5.
2. Используемую команду.
3. Дату и время ввода команды.
4. Город, который выбрал пользователь.

### Кнопка Настройки
После нажатия кнопки у пользователя выводится выбор с изменения:
1. Изменить валюту и изменить количество человек.

После нажатия кнопки 'Изменить валюту':
1. Выдается список возможных вариантов валюты в виде inline-клавиатуры.
2. Сообщение об успешном изменении.

После нажатия кнопки 'Изменить количество человек' у пользователя запрашивается:
1. Количества взрослых человек от 1 до 3.
2. Количества детей от 0 до 3.
3. Возраст детей в формате age-...-age от 1 до 17.

### Кнопка Помощь

## Requirements

- pyTelegramBotAPI==4.9.0
- python-dotenv==0.21.1
- pip==23.0.1
- wheel==0.36.2
- certifi==2022.12.7
- requests==2.28.2
- idna==2.10
- urllib3==1.26.15
- setuptools==65.5.0
- loguru==0.6.0
- translate==3.6.1
- beautifulsoup4==4.12.2

Для установки вышеприведенных библиотек выполните следующую команду: pip install -r requirements.txt
