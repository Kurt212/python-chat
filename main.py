import socket
import argparse
from connection import SocketConnection
from visualize import GUIVisual
from logic import ChatLogic
from user_input import GUIInput
import tkinter
from tkinter import scrolledtext

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

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
	main_window = tkinter.Tk()
	main_window.title("Chat")
	main_window.resizable(False, False)

	chat_text_widget = scrolledtext.ScrolledText(main_window, font=FONT, takefocus=0, width=60, state="disabled")
	chat_text_widget.grid(row=0, column=0, columnspan=2)

	message_entry = tkinter.Entry(main_window, font=FONT, width=55)
	message_entry.grid(row=1, column=0)
	message_entry.focus()

	visualize = GUIVisual(chat_text_widget)

	main_logic = ChatLogic(
		login=args.login,
		connection=connection,
		visualize=visualize,
	)

	user_input = GUIInput(main_logic, message_entry)

	message_entry_btn = tkinter.Button(
		main_window,
		text="Отправить",
		font=FONT_BOLD,
		command=user_input.on_text_entered,
	)
	message_entry_btn.grid(row=1, column=1)

	def enter_event(_):
		user_input.on_text_entered()

	main_window.bind("<Return>", enter_event)

	main_logic.start()

	main_window.mainloop()

if __name__ == "__main__":
	main()
