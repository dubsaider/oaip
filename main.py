import requests
import os
import time

from typing import Optional, Dict, List, BinaryIO

from dotenv import load_dotenv 

from handlers.hello_handler import Handler
from handlers.button_handler import ButtonHandler
from handlers.picture_handler import PictureHandler


class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.offset = 0
        self.handlers = [Handler(), ButtonHandler(), PictureHandler()]

    def _request(self, method: str, params: Optional[Dict] = None) -> Dict:
        """Базовый метод для запросов к API"""
        url = f"{self.base_url}/{method}"
        try:
            if params:
                response = requests.post(url, json=params)
            else:
                response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return {"ok": False, "error": str(e)}
        
    def _process_message(self, message: Dict):
        """Обработать одно сообщение"""
        for handler in self.handlers:
            try:
                handler(message, self)
            except Exception as e:
                print(f"Ошибка в обработчике: {e}")
        
    def get_me(self) -> Dict:
        """Получить информацию о боте"""
        return self._request("getMe")
    
    def send_message(self, chat_id: int, text: str, 
                     inline_keyboard: Optional[dict] = None,
                     parse_mode: Optional[str] = None) -> Dict:
        """Отправить текстовое сообщение"""
        params = {
            "chat_id": chat_id,
            "text": text
        }
        if parse_mode:
            params["parse_mode"] = parse_mode
        if inline_keyboard:
            params["reply_markup"] = inline_keyboard
        return self._request("sendMessage", params)
    
    def get_updates(self, timeout: int = 30) -> List[Dict]:
        """Получить новые обновления"""
        params = {
            "offset": self.offset,
            "timeout": timeout,
            "allowed_updates": ["message", "callback_query"]
        }
        response = self._request("getUpdates", params)
        
        if response.get("ok") and response.get("result"):
            updates = response["result"]
            if updates:
                # Обновляем offset для следующего запроса
                self.offset = updates[-1]["update_id"] + 1
            return updates
        return []
    
    def send_photo(self, chat_id: int, photo: BinaryIO,
                   caption: Optional[str] = None) -> Dict:

        url = f"{self.base_url}/sendPhoto"
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption

        files = {'photo': photo}

        try:
            if files:
                response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка отправки фото: {e}")
            return {"ok": False, "error": str(e)}
        
    def get_file(self, file_id: str) -> Dict:
        """Получить информацию о файле"""
        return self._request("getFile", {"file_id": file_id})
    
    def download_file(self, file_path: str, new_filename: str = None) -> bool:
        url = f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()

            if not new_filename:
                new_filename = file_path.split('/')[-1]

            with open(new_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return True
        except Exception as e:
            print(f'Ошибка скачивания: {e}')
            return False


    def run_polling(self):
        """Запустить long polling"""
        print("Бот запущен...")
        
        while True:
            try:
                updates = self.get_updates()
                
                for update in updates:
                    if "message" in update:
                        message = update["message"]
                        self._process_message(message)
                    if "callback_query" in update:
                        callback_query = update["callback_query"]
                        self._process_message(callback_query)
                
                time.sleep(1)
                
            except KeyboardInterrupt:
                print("\nБот остановлен")
                break
            except Exception as e:
                print(f"Ошибка в polling: {e}")
                time.sleep(1)

load_dotenv()

bot = TelegramBot(os.getenv('TELEGRAM_TOKEN'))

bot.run_polling()