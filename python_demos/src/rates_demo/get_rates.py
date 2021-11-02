""" get rates """

from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import requests

from rates_demo.business_days import business_days

def get_rates() -> None:
    """ get rates """

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    rate_responses: list[str] = []

    currency_symbols = ['USD', 'CAD', 'GBP']

    for business_day in business_days(start_date, end_date):

        rate_url = "".join([
            "http://127.0.0.1:5000/api/",
            str(business_day),
            "?base=USD&" + ",".join(currency_symbols)
        ])

        response = requests.get(rate_url)
        rate_responses.append(response.text)

    print("\n".join(rate_responses))


def get_rate_task(business_day: date):
    """ get rate task """

    rate_url = "".join([
        "http://127.0.0.1:5000/api/",
        str(business_day),
        "?base=USD&symbols=EUR"
    ])

    response = requests.get(rate_url)
    return response.text


def get_rates_threadpool() -> None:
    """ get rates threadpool """

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    rate_responses: list[str] = []

    with ThreadPoolExecutor() as executor:
        rate_responses = list(executor.map(
            get_rate_task,
            [ business_day for business_day
              in business_days(start_date, end_date) ]))

    print("".join(rate_responses))



