""" simple query """

import pyodbc

from db_demos.conn_info  import conn_string


def run() -> None:
    """ run """
    
    with pyodbc.connect(conn_string) as conn:

        rates = conn.execute(
            "select currencysymbol as currency_symbol from rates")

        for rate_row in rates:
            print(rate_row.currency_symbol)


if __name__ == "__main__":
    run()