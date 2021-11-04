""" rate server module """

from typing import Optional, Any
from multiprocessing.sharedctypes import Synchronized
import multiprocessing as mp
import sys
import socket
import threading
import re
import json
import requests

CLIENT_COMMAND_PARTS = [
    r"^(?P<name>[A-Z]*) ",
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) ",
    r"(?P<symbol>[A-Z]{3})$"
]

CLIENT_COMMAND_REGEX = re.compile("".join(CLIENT_COMMAND_PARTS))

# Task 1 - Cache Rate Results

# Upgrade the application to check the database for a given exchange rate
# (date, currency)

# If the exchange rate was previously retrieved and stored in the
# database (inside the rates table), then return it

# If the exchange rate is not in the database, then download it, add it to
# the database and return it

# Task 2 - Clear Rate Cache

# Add a command for clearing the rate cache from the server command
# prompt. Name the command "clear".

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
                data = self.conn.recv(2048)

                if not data:
                    break

                client_command_str: str = data.decode("UTF-8")

                client_command_match = CLIENT_COMMAND_REGEX.match(
                    client_command_str
                )

                if not client_command_match:
                    self.conn.sendall(b"Invalid Command Format")
                else:
                    self.process_client_command(
                        client_command_match.groupdict())

        except ConnectionAbortedError:
            pass
            # ...

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1
    
    def process_client_command(self, client_command: dict[str, Any]) -> None:
        """ process client command """

        if client_command["name"] == "GET":

            url = "".join([
                "http://localhost:5000/api/",
                client_command["date"],
                "?base=USD&symbols=",
                client_command["symbol"]
            ])

            response = requests.get(url)

            # rate_data = json.loads(response.text)
            rate_data = response.json()

            self.conn.sendall(
                str(rate_data["rates"][client_command["symbol"]])
                .encode("UTF-8")
            )

        else:
            self.conn.sendall(b"Invalid Command Name")



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