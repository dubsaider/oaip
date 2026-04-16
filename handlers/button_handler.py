class ButtonHandler:
    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        message, bot = args[0], args[1]
        chat_id = message['message']['chat']['id']
        message = message['data']

        if message in ('red', 'blue'):
            if message == 'red':
                bot.send_message(chat_id, 'Выбрана красная')
            elif message == 'blue':
                bot.send_message(chat_id, 'Выбрана синяя')