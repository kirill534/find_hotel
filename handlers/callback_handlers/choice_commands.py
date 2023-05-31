import datetime
import keyboards.inline.currencies_buttons
from loader import bot
from loguru import logger
from telebot.types import CallbackQuery
from states.user_states import UserInputState



@bot.callback_query_handler(
    func=lambda call: call.data.startswith(
        ("lowprice", "highprice", "bestdeal", "settings", "help", "start", "history")
    )
)
def commands_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку "lowprice"/"highprice"/"bestdeal"/"settings"/"help"/"start"/"history"
    : param call: "lowprice"/"highprice"/"bestdeal"/"settings"/"help"/"start"/"history"
    : return : None
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)
    logger.info("Нажата кнопка: " + call.data)
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data.startswith(("lowprice", "highprice", "bestdeal")):
            data["command_buttons"] = call.data
            data["date_time"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            if data["save_info"] == "Нет":
                bot.set_state(call.message.chat.id, UserInputState.input_city)
                bot.send_message(
                    call.message.chat.id, "Введите город в котором нужно найти отель: "
                )
            else:
                if call.data.startswith(("lowprice", "highprice")):
                    keyboards.inline.check_info.buttons_info(call.message, data)
                else:
                    bot.set_state(call.message.chat.id, UserInputState.priceMin)
                    bot.send_message(
                        call.message.chat.id,
                        f'Введите минимальную стоимость отеля в {data["currencies_sign"]}.',
                    )

        elif call.data == "settings":
            keyboards.inline.settings_buttons.show_buttons_settings(
                call.message, data
            )

        elif call.data == "help":
            keyboards.inline.exit_buttons.buttons_exit(
                call.message,
                text="Привет\n"
                f"Данный бот разработан в рамках дипломного проекта.\n"
                f"На данный момент бот умеет следующие основные 3 "
                f"функции взаимодействия с сайтом Hotels.com:\n\n"
                f"Дешевые - Узнать топ самых дешевых отелей в городе.\n"
                f"Дорогие - Узнать топ самых дорогих отелей в городе.\n"
                f"С ценой - Узнать топ отелей наиболее подходящих по цене и расположению от цента.\n\n"
                f"- В настройках вы можете поменять валюту в которой будет выводиться цена за проживание.\n"
                f"- В истории вы можете увидеть историю поисков отелей, когда количество запросов достигнет"
                f" 5 последний будет удаляться\n\n"
                f"- Перед отправлением запроса вы сможете увидеть все параметры, а так же сможете изменить их.\n"
                f"- Кнопка 'Сохранить' сохраняет все параметры чтобы в дальнейшем их не вводить\n\n"
                f"Поиск для городов России не работает\n",
            )

        elif call.data == "history":
            logger.info(f"Выбрана команда history! User_id: {call.message.chat.id}")
            keyboards.reply.number_requests.buttons_number(call.message)
