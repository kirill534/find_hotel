import sqlite3
from telebot.types import Message
from loguru import logger


def add_user(message: Message) -> None:
    """
    Создает базу данных если её еще нет.
    : param message : Message
    : return : None
    """
    with sqlite3.connect("hotel_db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS User(
            UserID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            ChatID INTEGER UNIQUE,
            UserName STRING,
            FullName TEXT
        );
        """
        )
        try:
            cursor.execute(
                "INSERT INTO User (ChatID, UserName, FullName) VALUES (?, ?, ?)",
                (
                    message.chat.id,
                    message.from_user.username,
                    message.from_user.full_name,
                ),
            )
            logger.info(f"Добавлен новый пользователь. UserID: {message.chat.id}")
        except sqlite3.IntegrityError:
            logger.info(
                f"Данный пользователь уже существует. UserID: {message.chat.id}"
            )


def add_query(query_data: dict) -> None:
    """
    Создаёт таблицу, если она ещё не создавалась и добавляет туда данные,
    с результатом для поиска отелей.
    : param query_data : dict
    : return : None
    """

    with sqlite3.connect("hotel_db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Query(
            QueryID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            UserID INTEGER,
            QueryCounter INTEGER,
            Command STRING,
            DateTime STRING, 
            InputCity STRING,
            DestinationID STRING,
            PhotoNeed STRING,
            FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE
            
        );    
        """
        )
        try:
            cursor.execute(
                f"SELECT `UserID` FROM User WHERE `ChatID` = ?",
                (query_data["user_id"],),
            )
            user_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO Query(UserID, QueryCounter, Command, InputCity, PhotoNeed, DestinationID, DateTime)"
                " VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    query_data["query_counter"],
                    query_data["command_buttons"],
                    query_data["city"],
                    query_data["photo_need"],
                    query_data["destination_id"],
                    query_data["date_time"],
                ),
            )
            logger.info(f"В БД добавлен новый запрос. UserID: {user_id}")

            cursor.execute(
                f"""
                    DELETE FROM Query WHERE Query.[DateTime]=
                    (SELECT MIN([DateTime]) FROM Query WHERE `UserID` = '{user_id}' )
                    AND
                    ((SELECT COUNT(*) FROM Query WHERE `UserID` = '{user_id}' ) > 5 ) 
                """
            )
        except sqlite3.IntegrityError:
            logger.info(
                f"Запрос с такой датой и временем уже существует. UserID: {user_id}"
            )


def add_response(search_result: dict) -> None:
    """
    Создаёт таблицу, если она ещё не создавалась и добавляет туда данные,
    с результатом поиска отелей.
    : param search_result : dict
    : return : None
    """
    with sqlite3.connect("hotel_db.sqlite3") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS Response(
                ResponseID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                QueryID INTEGER,
                RequestNumber INTEGER,
                HotelID STRING,
                InputCity STRING,
                Name STRING,
                Address STRING, 
                Price REAL,
                CurrenciesSign STRING,
                Distance REAL,
                HotelLink STRING,
                FOREIGN KEY (RequestNumber) REFERENCES Query(QueryCounter) ON DELETE CASCADE ON UPDATE CASCADE
            );
            """
        )
        for item in search_result.items():
            cursor.execute(
                f"SELECT `QueryCounter` FROM Query WHERE `DateTime` = ?",
                (item[1]["date_time"],),
            )
            request_number = cursor.fetchone()[0]

            cursor.execute(
                f"SELECT `QueryID` FROM Query WHERE `DateTime` = ?",
                (item[1]["date_time"],),
            )
            query_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO Response(QueryID, RequestNumber, HotelID, InputCity, Name, Address,"
                " Price, CurrenciesSign, Distance, HotelLink) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    query_id,
                    request_number,
                    item[0],
                    item[1]["input_city"],
                    item[1]["name"],
                    item[1]["address"],
                    item[1]["price"],
                    item[1]["currencies_sign"],
                    round(item[1]["distance"] * 1.609344, 2),
                    item[1]["hotel_link"],
                ),
            )
            logger.info(f'В БД добавлены данные отеля. UserID: {item[1]["user_id"]}')

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS Images(
            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            HotelID INTEGER REFERENCES response (id),
            Link TEXT,
            FOREIGN KEY (HotelID) REFERENCES Response(HotelID) ON DELETE CASCADE ON UPDATE CASCADE     
            );"""
            )
            for link in item[1]["images"]:
                cursor.execute(
                    "INSERT INTO Images (HotelID, Link) VALUES (?, ?)", (item[0], link)
                )
            logger.info(
                f'В БД добавлены ссылки на фотографии отеля. UserID: {item[1]["user_id"]}'
            )
