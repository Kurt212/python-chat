import socket
import threading


class Connection:
    def read(self) -> str:
        pass

    def write(self, s: str):
        pass


class SocketConnection(Connection):
    def __init__(self, sck: socket.socket):
        self.socket = sck

        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    def _receive(self, msg_len):
        chunks = []
        bytes_recd = 0
        while bytes_recd < msg_len:
            chunk = self.socket.recv(min(msg_len - bytes_recd, 2048))

            if chunk == b'':
                raise RuntimeError("socket connection broken")

            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        return b''.join(chunks)

    def _send(self, msg_bytes):
        total_sent = 0
        msg_len = len(msg_bytes)

        while total_sent < msg_len:
            sent = self.socket.send(msg_bytes[total_sent:])

            if sent == 0:
                raise RuntimeError("socket connection broken")

            total_sent += sent

    def read(self) -> str:
        """
            Каждое сообщение будет декодироваться в utf-8 из голых байтов
            И потом будет возвращаться из метода

            Алгоритм прочтения сообщений:
                1. Читаем заголовок из 4 байтов. Это число int32 сколько байтов в сообщении
                2. Читаем эти N байтов сообщения по 2048 байт за чанк.
                3. Собираем все прочитанные чанки в итоговое сообщение и декодируем в utf-8 строку
        """
        with self.read_lock:
            header_bytes = self._receive(4)
            body_length = int.from_bytes(header_bytes, byteorder='little')

            body = self._receive(body_length)
            result_str = body.decode("utf-8")

            return result_str

    def write(self, s: str):
        """
            Каждое сообщение интерпретируем как utf-8 строчку и кодируем в utf-8 байты
            Длину сообщения кодируем как 4 байтовое число в little-endian
            Сначала шлем заголовок - 4 байта, потом байты сообщения
        """
        with self.write_lock:
            body_bytes = s.encode('utf-8')

            body_length = len(body_bytes)
            header_bytes = body_length.to_bytes(4, 'little')

            self._send(header_bytes)
            self._send(body_bytes)
