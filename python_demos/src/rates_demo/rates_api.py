""" rates api """

from typing import Any
import pathlib
import csv
import math
from flask import Flask, Response, request

rates: list[dict[str,Any]] = []


app = Flask(__name__)

@app.route("/check")
def check() -> Response:
    """ health check endpoint """
    return "READY"


@app.route("/api/<rate_date>")
def rates_by_date(rate_date: str) -> Response:
    """ rates_by_date """

    for rate in rates:

        if rate["Date"] == rate_date:

            base_country = request.args.get("base", "EUR")

            if "symbols" in request.args:
                country_symbols = request.args["symbols"].split(",")
            else:
                country_symbols = [ col for col in rate if col != "Date"]
            
            






"""

URL: http://localhost/api/2021-04-08?base=INR&symbols=USD,EUR

{
    "date": "2021-04-08",
    "base": "INR",
    "rates": [
        { "USD": 70 },
        { "EUR": 80 },
    ]
}


"""    


def load_rates_from_history(
    rates_file_path: pathlib.Path) -> list[dict[str,Any]]:
    """ load rates from history """

    rates_history: list[dict[str,Any]] = []

    with open(rates_file_path, encoding="UTF-8") as rates_file:

        rates_file_csv = csv.DictReader(rates_file)

        for rate_row in rates_file_csv:

            rate_entry = { "Date": rate_row["Date"], "EUR": 1.0 }

            for rate_col in rate_row:
                if rate_col != "Date" and len(rate_col) > 0:
                    if rate_row[rate_col] == "N/A":
                        rate_entry[rate_col] = math.nan
                    else:
                        rate_entry[rate_col] = float(rate_row[rate_col])

            rates_history.append(rate_entry)

    return rates_history



def start_rates_api() -> None:
    """ start rates api """

    global rates

    rates_file_path = pathlib.Path("..", "data", "eurofxref-hist.csv")

    rates = load_rates_from_history(rates_file_path)

    app.run()

