import sqlite3
from loguru import logger


def read_query(user: int) -> list:
    """
    Принимает id пользователя, делает запрос к базе данных, получает в ответ
    результаты запросов данного пользователя.
    : param user : int
    : return : list
    """
    logger.info(f"Читаем таблицу query. UserID: {user}")
    with sqlite3.connect("hotel_db.sqlite3") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT `Command`, `QueryCounter`, `DateTime`, `InputCity` "
                "FROM Query "
                "JOIN User ON Query.UserID = User.UserID "
                "WHERE User.ChatID = ?",
                (user,),
            )
            records = cursor.fetchall()
            return records
        except sqlite3.OperationalError:
            logger.info(f"В базе данных пока нет таблицы с запросами. UserID: {user}")
            return []


def get_history_response(message) -> dict:
    """
    Принимает id-запроса, обращается к базе данных и выдает данные которые нашел бот для
    пользователя по его запросам.
    : param query : str
    : return : dict
    """
    logger.info(f"Читаем таблицу response. UserID: {message.chat.id}")
    with sqlite3.connect("hotel_db.sqlite3") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT Response.* FROM Response "
                "JOIN Query ON Response.QueryID = Query.QueryID "
                "JOIN User ON Query.UserID = User.UserID "
                "WHERE User.ChatID = ? and Query.QueryCounter = ? ",
                (message.chat.id, message.text, ),
            )
            records = cursor.fetchall()
            history = {}
            for item in records:
                hotel_id = item[3]
                history[item[3]] = {
                    "input_city": item[4],
                    "name": item[5],
                    "address": item[6],
                    "price": item[7],
                    "currencies_sign": item[8],
                    "distance": item[9],
                    "hotel_link": item[10],
                }
                cursor.execute("SELECT * FROM Images WHERE `HotelID` = ?", (hotel_id,))
                images = cursor.fetchall()
                links = []
                for link in images:
                    links.append(link[2])
                history[item[3]]["images"] = links

            return history
        except sqlite3.OperationalError:
            logger.info(
                f"В базе данных пока нет таблицы с запросами. UserID: {message.chat.id}"
            )
            return {}
