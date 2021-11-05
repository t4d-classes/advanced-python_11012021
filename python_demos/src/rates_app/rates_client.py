""" rate client module """
import sys
import socket
import yaml
import pathlib
from typing import Any

def read_config() -> Any:
    """ read config """

    with open(pathlib.Path("config", "rates_config.yaml")) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

config = read_config()

try:

    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM) as socket_client:

        host = config['server']['host']
        port = int(config['server']['port'])        

        socket_client.connect( (host, port) )

        welcome_message = socket_client.recv(2048)

        print(welcome_message.decode('UTF-8'))

        while True:

            command = input("> ")

            if command == "exit":
                break
            else:
                socket_client.sendall(command.encode('UTF-8'))
                print(socket_client.recv(2048).decode('UTF-8')) 

except ConnectionResetError:
    print("Server connection was closed.")

except KeyboardInterrupt:
    pass

sys.exit(0)