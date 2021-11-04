""" simple query """

import pyodbc

from db_demos.conn_info  import conn_string


def run() -> None:
    """ run """
    
    with pyodbc.connect(conn_string) as conn:

        with conn.cursor() as cur:

            cur.execute("select * from rates")

            rate = cur.fetchone()

            if rate:
                print(rate)
            else:
                print("no rate found")

            rate = cur.fetchone()

            if rate:
                print(rate)
            else:
                print("no rate found")


if __name__ == "__main__":
    run()