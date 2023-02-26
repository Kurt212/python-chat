from datetime import datetime
from tkinter.scrolledtext import ScrolledText
import tkinter


class Visual:
    def show_message(self, login: str, message: str):
        pass


class GUIVisual(Visual):
    def __init__(self, chat_box: ScrolledText):
        self.chat_box = chat_box

    def show_message(self, login: str, message: str):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        result = f"[{time}] {login}: {message}"

        self.chat_box.configure(state="normal")

        self.chat_box.insert(tkinter.END, result + "\n")

        self.chat_box.configure(state="disabled")
        self.chat_box.see(tkinter.END)



class TerminalVisual(Visual):
    def show_message(self, login: str, message: str):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        result = f"[{time}] {login}: {message}"

        print(result)
