""" rate server module """

from typing import Optional, Any
from multiprocessing.sharedctypes import Synchronized
import multiprocessing as mp
import sys
import socket
import threading
import re
import requests
import pyodbc
from datetime import datetime, date
from decimal import Decimal
import yaml
import pathlib
import csv

from rates_shared.utils import (
    parse_command, read_config, CURRENCY_SYMBOLS_REGEX)

config = read_config()

docker_conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    f"SERVER={config['database']['server']}",
    f"DATABASE={config['database']['database']}",
    f"UID={config['database']['username']}",
    f"PWD={config['database']['password']}",
]

conn_string = ";".join(docker_conn_options)



def log_client_event(thread_id: Optional[int], host: str, port: int, msg: str):

    with open(pathlib.Path("logs", "server_log.csv"),
        "a", newline="\n") as csv_file:

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow((thread_id, datetime.now(), host, port, msg))


def get_rate_from_api(closing_date: date, currency_symbol: str,
                      currency_rates: list[tuple[date, str, Decimal]]) -> None:
    """ get rate from api """

    url = "".join([
        "http://localhost:5000/api/",
        closing_date.strftime("%Y-%m-%d"),
        "?base=USD&symbols=",
        currency_symbol,
    ])

    response = requests.get(url)
    rate_data = response.json()

    currency_rates.append(
        (closing_date,
         currency_symbol,
         Decimal(str(rate_data["rates"][currency_symbol]))))


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

                client_command_dict = parse_command(client_command_str)

                if not client_command_dict:
                    self.conn.sendall(b"Invalid Command Format")
                else:
                    self.process_client_command(client_command_dict)

        # except ConnectionAbortedError:
        #     pass

        # except OSError:
        #     pass

        except:
            pass

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1
    
    def process_client_command(self, client_command: dict[str, Any]) -> None:
        """ process client command """

        if client_command["name"] == "GET":

            with pyodbc.connect(conn_string) as con:

                closing_date = datetime.strptime(
                    client_command["date"], "%Y-%m-%d")

                currency_symbols = CURRENCY_SYMBOLS_REGEX.split(
                    client_command["symbol"])

                rate_sql_params: list[Any] = [closing_date]
                rate_sql_params.extend(currency_symbols)

                placeholders = ",".join("?" * len(currency_symbols))

                rate_sql = " ".join([
                    "select exchangerate as exchange_rate,"
                    "currencysymbol as currency_symbol from rates",
                    "where closingdate = ? and "
                    f"currencysymbol in ({placeholders})"
                ])

                cached_currency_symbols: set[str] = set()

                rate_responses = []

                with con.cursor() as cur:

                    for rate in cur.execute(rate_sql, rate_sql_params):
                        cached_currency_symbols.add(rate.currency_symbol)
                        rate_responses.append(
                            f"{rate.currency_symbol}: {rate.exchange_rate}")

                currency_rate_threads: list[threading.Thread] = []
                currency_rates: list[tuple[date, str, Decimal]] = []

                for currency_symbol in currency_symbols:
                    if currency_symbol not in cached_currency_symbols:

                        currency_rate_thread = threading.Thread(
                            target=get_rate_from_api,
                            args=(closing_date,
                                  currency_symbol, currency_rates))

                        currency_rate_thread.start()
                        currency_rate_threads.append(currency_rate_thread)

                for currency_rate_thread in currency_rate_threads:
                    currency_rate_thread.join()

                if len(currency_rates) > 0:

                    with con.cursor() as cur:

                        sql = " ".join([
                            "insert into rates",
                            "(closingdate, currencysymbol, exchangerate)",
                            "values",
                            "(?, ?, ?)",
                        ])

                        cur.executemany(sql, currency_rates)

                    for currency in currency_rates:
                        rate_responses.append(
                            f"{currency[1]}: {currency[2]}")



                self.conn.sendall(
                    "\n".join(rate_responses).encode("UTF-8"))

        else:
            self.conn.sendall(b"Invalid Command Name")



def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        
        socket_server.bind( (host, port) )
        socket_server.listen()

        while True:

            conn, addr = socket_server.accept()

            with client_count.get_lock():
                client_count.value += 1

            client_con_thread = ClientConnectionThread(conn, client_count)
            client_con_thread.start()

            log_client_event(
                client_con_thread.ident,
                addr[0],
                addr[1],
                "connect")


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

def command_clear_cache() -> None:
    """ command clear cache """

    with pyodbc.connect(conn_string) as con:
        con.execute("delete from rates")

    print("cache cleared")


def command_exit(server_process: Optional[mp.Process]) -> None:
    """ exit the rates server app """

    if server_process and server_process.is_alive():
        server_process.terminate()


def main() -> None:
    """Main Function"""

    try:

        client_count: Synchronized = mp.Value('i', 0)
        server_process: Optional[mp.Process] = None
        
        host = config['server']['host']
        port = int(config['server']['port'])

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, host, port, client_count)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "count":
                command_count(client_count)
            elif command == "clear":
                command_clear_cache()
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