from .abstract_handler import AbstractHandler

class FileHandler(AbstractHandler):
    def __call__(self, *args, **kwds):
        message, bot = args[0], args[1]
        file_id = self.parser(message)
        
        if file_id is not None:
            file_path = bot.get_file(file_id)['result']['file_path']
            
            print(bot.download_file(file_path))