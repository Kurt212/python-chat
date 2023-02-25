from datetime import datetime


class Visual:
    def show_message(self, login: str, message: str):
        pass


class TerminalVisual(Visual):
    def show_message(self, login: str, message: str):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")

        result = f"[{time}] {login}: {message}"

        print(result)
