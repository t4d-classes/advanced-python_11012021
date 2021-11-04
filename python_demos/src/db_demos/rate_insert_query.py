""" rate insert query """

import pyodbc

from db_demos.conn_info  import conn_string


def run() -> None:
    """ run """
    
    with pyodbc.connect(conn_string) as conn:

        closing_date = "2021-10-3"
        currency_symbol = "HKD"
        exchange_rate = 2.34

        conn.execute(
            "insert into rates (ClosingDate, CurrencySymbol, ExchangeRate) "
            "values (?, ?, ?)",
            (closing_date, currency_symbol, exchange_rate))

if __name__ == "__main__":
    run()