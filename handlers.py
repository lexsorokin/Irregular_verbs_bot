import time
from user_search_config import UserSearchConfig
from loader import IrregularVerbs_bot
from irregular_verbs_data import irregular_verbs
from telebot import types


@IrregularVerbs_bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    user = UserSearchConfig.get_user(message.chat.id)
    user.messages_to_delete.append(message.message_id)
    if message.text == '/start':
        get_forms = IrregularVerbs_bot.send_message(chat_id=message.chat.id,
                                                    text=f'Привет, {message.from_user.first_name}😘\n'
                                                         '<b>\nВведи первую форму глагола</b>⤵\n'
                                                         '\n<i>PS</i> После поиска рекомендую нажать кнопку '
                                                         '<b>Закончить '
                                                         'Поиск</b>, чтобы очистить диалог🤓',
                                                    parse_mode='HTML')
        user.messages_to_delete.append(get_forms.message_id)
        IrregularVerbs_bot.register_next_step_handler(get_forms, get_forms_res)


def get_forms_res(message):
    user = UserSearchConfig.get_user(message.chat.id)
    user.messages_to_delete.append(message.message_id)
    verb = message.text.lower()
    if verb in irregular_verbs:
        res = f'<i>1-я Форма</i>: <b>{verb}</b>\n' \
              f'<i>2-я Форма</i>: <b>{irregular_verbs[verb]["forms"][0]}</b>\n'\
              f'<i>3-я Форма</i>: <b>{irregular_verbs[verb]["forms"][1]}</b>\n' \
              f'\n<i>Перевод</i>: <b>{irregular_verbs[verb]["translation"]}</b>'
        mark_up_search = types.InlineKeyboardMarkup(row_width=1)
        google_voice_first_form = types.InlineKeyboardButton(text=f'Прослушать - {verb}',
                                                             url=f'https://translate.google.ru/?sl=en&tl=ru&text={verb}&op=translate')
        google_voice_second_form = types.InlineKeyboardButton(
            text=f'Прослушать - {irregular_verbs[verb]["forms"][0]}',
            url=f'https://translate.google.ru/?sl=en&tl=ru&text={irregular_verbs[verb]["forms"][0]}&op=translate')
        google_voice_third_form = types.InlineKeyboardButton(
            text=f'Прослушать - {irregular_verbs[verb]["forms"][1]}',
            url=f'https://translate.google.ru/?sl=en&tl=ru&text={irregular_verbs[verb]["forms"][1]}&op=translate')
        exit_btn = types.InlineKeyboardButton(text='Закончить поиск', callback_data='exit')
        mark_up_search.add(google_voice_first_form, google_voice_second_form, google_voice_third_form, exit_btn)
        res_mes = IrregularVerbs_bot.send_message(chat_id=message.chat.id,
                                                  text=res,
                                                  reply_markup=mark_up_search,
                                                  parse_mode='HTML')
        user.messages_to_delete.append(res_mes.message_id)
    else:
        mark_up_exit = types.InlineKeyboardMarkup(row_width=2)
        exit_btn = types.InlineKeyboardButton(text='Закончить поиск', callback_data='exit')
        mark_up_exit.add(exit_btn)
        search_again = IrregularVerbs_bot.send_message(chat_id=message.chat.id,
                                                       text='Введенное слово не является неправильным глаголов.\n'
                                                            'Введи глагол снова или закончи поиск.',
                                                       reply_markup=mark_up_exit)
        user.messages_to_delete.append(search_again.message_id)
        IrregularVerbs_bot.register_next_step_handler(search_again, get_forms_res)


@IrregularVerbs_bot.callback_query_handler(func=lambda callback: callback.data == 'exit')
def exit_search(callback):
    user = UserSearchConfig.get_user(callback.message.chat.id)
    exit_mes = IrregularVerbs_bot.send_message(chat_id=callback.message.chat.id,
                                               text='Пока😘')
    user.messages_to_delete.append(exit_mes.message_id)
    time.sleep(1)
    for message_id in user.messages_to_delete:
        IrregularVerbs_bot.delete_message(chat_id=callback.message.chat.id,
                                          message_id=message_id)
    user.messages_to_delete.clear()

