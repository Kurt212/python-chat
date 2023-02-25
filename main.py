import socket
import argparse
from connection import SocketConnection
from visualize import TerminalVisual
from logic import ChatLogic
from user_input import TerminalInput


def main():
	parser = argparse.ArgumentParser(prog='Chat', description='Делает чат')

	parser.add_argument('-s', '--server', help="запустить чат в режиме сервера", action='store_true')
	parser.add_argument('-c', '--client', help="запустить чат в режиме клиента", action='store_true')

	parser.add_argument('-p', '--port', help="порт по которому будет происходить подключение к чату", type=int)
	parser.add_argument('-a', '--address', help="ip адрес чата в режиме клиента")

	parser.add_argument('--login', help="Логин в чате")

	args = parser.parse_args()

	server_mode = args.server
	client_mode = args.client

	if server_mode and client_mode:
		raise ValueError("Нельзя запускать одновременно в обоих режимах")

	if not server_mode and not client_mode:
		raise ValueError("Необходимо выбрать один из режимов -s или -c")

	if args.login is None or args.login == "":
		raise ValueError("Необходимо указать логин в чате")

	if server_mode:
		if args.port == 0:
			raise ValueError(f"Указан невалидный порт {args.port}")

		# create an INET, STREAMing socket
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# bind the socket to a public host, and a well-known port
		server_socket.bind(('', args.port))
		# become a server socket
		server_socket.listen(1)

		client_socket, address = server_socket.accept()

		connection = SocketConnection(client_socket)

	else:
		if args.port == 0 or args.address == "":
			raise ValueError(f"Указан невалидный порт или адрес: {args.address} {args.port}")

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((args.address, args.port))

		connection = SocketConnection(s)

	# инициализация всех остальных модулей программы
	# connection уже был создан либо по ветке клиента, либо по ветке сервера
	visualize = TerminalVisual()

	main_logic = ChatLogic(
		login=args.login,
		connection=connection,
		visualize=visualize,
	)

	user_input = TerminalInput(main_logic)

	main_logic.start()
	user_input.start()




if __name__ == "__main__":
	main()
