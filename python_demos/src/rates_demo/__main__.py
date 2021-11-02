""" main module """

from rates_demo.get_rates import get_rates_threadpool
from rates_demo.rates_api_server import rates_api_server

if __name__ == "__main__":

    with rates_api_server():

        get_rates_threadpool()
