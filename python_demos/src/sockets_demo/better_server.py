""" sockets demo server module """

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

    socket_server.bind(('127.0.0.1', 5000))
    socket_server.listen()

    print("server is listening on 127.0.0.1:5000")

    conn, addr = socket_server.accept()

    print("received connection")

    welcome_message_str = "Connected to the server."
    welcome_message_str_len = len(welcome_message_str)

    welcome_message_bytes = welcome_message_str.encode('UTF-8')
    welcome_message_bytes_len = len(welcome_message_bytes)
    bytes_sent = 0

    header = f"Content-Length: {welcome_message_str_len};"

    conn.sendall(header.encode('UTF-8'))

    # roughly the implementation send all
    while bytes_sent < welcome_message_bytes_len:
        bytes_sent = bytes_sent + conn.send(
            welcome_message_bytes[bytes_sent:])