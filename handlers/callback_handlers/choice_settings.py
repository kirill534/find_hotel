import keyboards
from loader import bot
from loguru import logger
from telebot.types import CallbackQuery
from states.user_states import UserInputState


@bot.callback_query_handler(
    func=lambda call: call.data.startswith(("currency", "quantity_people"))
)
def commands_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку 'currency'/'quantity_people'

    : param call: 'currency'/'quantity_people'
    : return : None
    """
    logger.info("Нажата кнопка для изменения: " + call.data)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    with bot.retrieve_data(call.message.chat.id) as data:
        if call.data == "currency":
            keyboards.inline.currencies_buttons.show_buttons_currencies(
                call.message, data
            )
        elif call.data == "quantity_people":
            bot.set_state(call.message.chat.id, UserInputState.adults)
            bot.send_message(call.message.chat.id, text="Введите количество взрослых (от 1 до 3):")