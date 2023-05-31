import keyboards.inline.menu_buttuns
from loader import bot
from telebot.types import Message
from loguru import logger
import database
from states.user_states import UserInputState


@bot.message_handler(state=UserInputState.select_number)
def input_number_query(message: Message) -> None:
    """
    Ввод пользователем номера запроса, которые есть в списке. Если пользователь введет
    неправильный номер или это будет "не цифры", то бот попросит повторить ввод.
    Запрос к базе данных нужных нам записей. Выдача в чат результата.
    : param message : Message
    : return : None
    """
    if message.text.isdigit():
        queries = database.read_from_db.read_query(message.chat.id)
        number_query = [item[1] for item in queries]

        if int(message.text) in number_query:
            logger.info(f"Посылаем запрос к базе данных. User_id: {message.chat.id}")
            history_dict = database.read_from_db.get_history_response(message)
            if history_dict:
                logger.info(
                    f"Выдаем результаты выборки из базы данных. User_id: {message.chat.id}"
                )
                for hotel in history_dict.items():
                    caption = (
                        f"🛎Название отеля: <a href='{hotel[1]['hotel_link']}'>{hotel[1]['name']}</a>🛎\n"
                        f"📍Адрес отеля: {hotel[1]['address']}📍\n"
                        f"💴Стоимость проживания в сутки: {hotel[1]['price']} {hotel[1]['currencies_sign']}💴\n"
                        f"🚕Расстояние до центра: {hotel[1]['distance']} км🚕"
                    )
                    keyboards.inline.exit_buttons.buttons_exit(message, caption)
            else:
                bot.send_message(
                    message.chat.id, text="Почему-то ответ пуст! Попробуйте другие операции."
                )
                logger.info(f"Почему-то ответ пуст! User_id: {message.chat.id}")
                bot.set_state(message.chat.id, None)
                keyboards.inline.menu_buttuns.show_buttons_commands(message)
        else:
            bot.send_message(
                message.chat.id,
                text="Ошибка! Вы ввели число, которого нет в списке! Повторите ввод!",
            )
    else:
        bot.send_message(message.chat.id, text="Ошибка! Вы ввели не число! Повторите ввод!")