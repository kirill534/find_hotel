import keyboards.inline.check_info
from loader import bot
from loguru import logger
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: call.data.startswith(('byn', 'rub', 'usd')))
def currencies_callback(call: CallbackQuery) -> None:
    """
    Пользователь нажал кнопку "BYN" или "RUB" или "USD"
    :param call: "byn" or "rub" or "usd"
    :return : None
    """
    logger.info('Нажата кнопка: ' + call.data)
    with bot.retrieve_data(call.message.chat.id) as data:
        data['currencies'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        if call.data == 'byn':
            data['currencies_sign'] = 'BY'

        elif call.data == 'rub':
            data['currencies_sign'] = 'RUS'

        elif call.data == 'usd':
            data['currencies_sign'] = '$'

    if data['flag_checking']:
        keyboards.inline.check_info.buttons_info(call.message, data)
    else:
        bot.send_message(call.message.chat.id, f'Изменение успешное. Валюта в {data["currencies"]}')
        keyboards.inline.menu_buttuns.show_buttons_commands(call.message)

