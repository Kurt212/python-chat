from connection import Connection
from visualize import Visual
import threading
import json


class ChatLogic:
    def __init__(self, login: str, connection: Connection, visualize: Visual):
        self.con = connection
        self.visual = visualize
        self.read_thread = threading.Thread(target=self._read_incoming_messages)

        self.my_login = login
        self.other_login = ""

    def start(self):
        """
            Запускает работу модуля ChatLogic
        """
        # создаю поток для слушания входящих сообщений
        self.read_thread.start()
        # посылаю собеседнику свой логин
        data = {
            "type": "login",
            "login": self.my_login
        }
        self._send_json(data)

    def _send_json(self, data: dict):
        s = json.dumps(data)
        self.con.write(s)

    def _read_incoming_messages(self):
        while True:
            message_raw = self.con.read()
            try:
                message = json.loads(message_raw)
            except json.JSONDecodeError:
                continue
            message_type = message["type"]

            if message_type == "login":
                new_login = message["login"]
                if new_login == "":
                    continue

                self.other_login = new_login

            elif message_type == "message":
                message_text = message["message"]

                if self.other_login == "":
                    continue

                self.visual.show_message(self.other_login, message_text)

    def new_message(self, message):
        data = {
            "type": "message",
            "message": message
        }
        self._send_json(data)

        self.visual.show_message(self.my_login, message)
