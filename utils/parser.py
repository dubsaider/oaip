class Parser:
    def __init__(self, type):
        self.type = type
        self.key_to_args = {
            'TEXT': self._process_text,
            'FILE': self._process_file,
            'BUTTON': self._process_button
        }
        self.func = self.key_to_args[type]

    def __call__(self, *args, **kwds):
        message = args[0]
        try:
            return self.func(message)
        except Exception as e:
            print(f'Необработанная ситуация: {e}')
        
    def _process_text(self, message):
        if 'text' in message:
            chat_id = message['chat']['id']
            text = message['text']

            return text, chat_id
        return None, None

    def _process_file(self, message):
        if 'photo' in message:
            file_id = message['photo'][3]['file_id']

            return file_id
        if 'video' in message:
            file_id = message['video']['file_id']

            return file_id
        
        if 'media' in message:
            file_id = message['media']['file_id']

            return file_id

    def _process_button(self, message):
        if 'data' in message:
            chat_id = message['message']['chat']['id']
            text = message['data']

            return text, chat_id
        return None, None