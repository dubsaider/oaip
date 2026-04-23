from utils.inline_keyboard_builder import InlineKeyboardBuilder
from .abstract_handler import AbstractHandler

class MessageHandler(AbstractHandler):
    def __call__(self, *args, **kwds):
        message, bot = args[0], args[1]
        message, chat_id = self.parser(message)
        builder = InlineKeyboardBuilder()
        
        if message is not None:
            if 'привет' in message:
                bot.send_message(chat_id, 'Привет')
            
            if 'картинк' in message:
                bot.send_photo(chat_id, open(r"C:\Users\user\Pictures\Chieftec_APS650C.jpg", "rb"))

            if 'кнопк' in message:
                inline_keyboard = builder.get_keyboard([
                    [("Синяя", "blue"), ("Красная", "red")]
                ])
                bot.send_message(chat_id, 'Синяя или красная?', inline_keyboard)