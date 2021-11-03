""" sockets server """

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
    
    socket_server.bind( ('127.0.0.1', 5025) )
    socket_server.listen()

    print("server is listening on 127.0.0.1:5025")

    conn, addr = socket_server.accept() # accept is the blocking call

    print(f"client at {addr[0]}:{addr[1]} connected")

    conn.sendall(b"Welcome to 127.0.0.1:5025!")
    # conn.sendall("Welcome to 127.0.0.1:5025!".encode("UTF-8"))

    while True:
        message  = conn.recv(2048).decode('UTF-8')
        print("recv: " + message)
        conn.sendall(message.encode('UTF-8'))   