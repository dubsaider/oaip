from .abstract_handler import AbstractHandler 

class ButtonHandler(AbstractHandler):
    def __call__(self, *args, **kwds):
        message, bot = args[0], args[1]
        message, chat_id = self.parser(message)

        if message is not None and message in ('red', 'blue'):
            if message == 'red':
                bot.send_message(chat_id, 'Выбрана красная')
            elif message == 'blue':
                bot.send_message(chat_id, 'Выбрана синяя')