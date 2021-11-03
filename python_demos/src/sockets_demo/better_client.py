""" socker demo client module """

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_client:

    socket_client.connect(('127.0.0.1', 5000))

    header_data_str = ""
    content_data_str = ""

    while True:
        header_data_bytes = socket_client.recv(4)
        header_data_str += header_data_bytes.decode('UTF-8')

        if ";" in header_data_str:
            header, content_data_str = header_data_str.split(";")
            break

    chars_expected = int(header.split(" ")[1])

    while len(content_data_str) < chars_expected:
        content_data_bytes = socket_client.recv(4)
        content_data_str += content_data_bytes.decode('UTF-8')

    print(content_data_str)