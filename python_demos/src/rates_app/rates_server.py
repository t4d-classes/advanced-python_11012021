""" rate server module """

from typing import Optional
from multiprocessing.sharedctypes import Synchronized
import multiprocessing as mp
import sys
import socket
import threading

# Add support for the following client command

# GET 2019-01-03 EUR

# GET is the command name
# 2019-01-03 is the date of the current rates to retrieve
# EUR is the currency symbol to retrieve, DO NOT USE USD

# Call the Rates API using the USD as the base to get the currency rate
# for the specified year

# Ideally your code will do the following:

# 1. Use a regular expression with named capture groups to extract parts
# of the command

# 2. Add a function named "process_client_command" to
# "ClientConnectionThread" that will process the parsed command including
# calling the API, extracting the API response, and send back the rate
# value to the client

# Data comes back as JSON

# *3. Send back an error message for an incorrectly formatted command or an
# unsupported command name (only the GET command is supported)

class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(
        self,
        conn: socket.socket,
        client_count: Synchronized) -> None:

        threading.Thread.__init__(self)
        self.conn = conn
        self.client_count = client_count

    def run(self) -> None:

        try:

            self.conn.sendall(b"Connected to the Rate Server")

            while True:
                message = self.conn.recv(2048)
                if not message:
                    break
                self.conn.sendall(message)

        except ConnectionAbortedError:
            pass
            # ...

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1



def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        
        socket_server.bind( (host, port) )
        socket_server.listen()

        while True:

            conn, _ = socket_server.accept()

            with client_count.get_lock():
                client_count.value += 1

            client_con_thread = ClientConnectionThread(conn, client_count)
            client_con_thread.start()


def command_start_server(
    server_process: Optional[mp.Process],
    host: str, port: int,
    client_count: Synchronized) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        server_process = mp.Process(
            target=rate_server, args=(host, port, client_count))
        server_process.start()
        print("server started")

    return server_process


def command_stop_server(
    server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")

    server_process = None

    return server_process

def command_server_status(server_process: Optional[mp.Process]) -> None:
    """ output the status of the server """

    # typeguard
    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is stopped")

def command_count(client_count: Synchronized) -> None:
    """ exit the rates server app """

    print(client_count.value)

def command_exit(server_process: Optional[mp.Process]) -> None:
    """ exit the rates server app """

    if server_process and server_process.is_alive():
        server_process.terminate()


def main() -> None:
    """Main Function"""

    try:

        client_count: Synchronized = mp.Value('i', 0)
        server_process: Optional[mp.Process] = None
        
        host = "127.0.0.1"
        port = 5050

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, host, port, client_count)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "count":
                command_count(client_count)
            elif command == "status":
                command_server_status(server_process)
            elif command == "exit":
                command_exit(server_process)
                break

    except KeyboardInterrupt:
        command_exit(server_process)

    sys.exit(0)


if __name__ == '__main__':
    main()