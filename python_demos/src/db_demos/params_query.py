""" params query """

import pyodbc

from db_demos.conn_info  import conn_string


def run() -> None:
    """ run """
    
    with pyodbc.connect(conn_string) as conn:

        # let's pretend this value is coming from user data
        currency_symbol = input("Please enter a currency symbol > ")

        rates = conn.execute(
            "select currencysymbol as currency_symbol "
            "from rates where currencysymbol = ?", (currency_symbol,))

        for rate_row in rates:
            print(rate_row.currency_symbol)


if __name__ == "__main__":
    run()