class PictureHandler:
    def __init__(self):
        pass

    def __call__(self, *args, **kwds):
        message, bot = args[0], args[1]

        file_id = message['photo'][3]['file_id']

        file_path = bot.get_file(file_id)['result']['file_path']
        
        print(bot.download_file(file_path))