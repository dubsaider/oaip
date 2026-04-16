class InlineKeyboardBuilder:
    def __init__(self):
        self.buttons = [] 
    
    def get_keyboard(self, keys):
        keyboard = []
        
        for row in keys:
            keyboard_row = []
            for button in row:
                if isinstance(button, tuple) and len(button) == 2:
                    keyboard_row.append({
                        "text": button[0],
                        "callback_data": button[1]
                    })
            
            if keyboard_row:  
                keyboard.append(keyboard_row)
        
        return {"inline_keyboard": keyboard}