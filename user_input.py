import sys
from logic import ChatLogic
import threading


class TerminalInput:
    def __init__(self, logic: ChatLogic):
        self.logic = logic
        self.user_input_thread = threading.Thread(target=self._read_user_input)

    def start(self):
        self.user_input_thread.start()

    def _read_user_input(self):
        while True:
            text = input()
            sys.stdout.write("\033[F")  # Cursor up one line
            self.logic.new_message(text)
