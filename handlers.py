from loader import IrregularVerbs_bot

@IrregularVerbs_bot.message_handler(commands=['start', 'help'])
def start_bot(message):
    if message.text == '/start':
        IrregularVerbs_bot.send_message(chat_id=message.chat.id,
                                        message='Привет')