""" rates api """

from flask import Flask, Response


app = Flask(__name__)

@app.route("/")
def home() -> Response:
    """ home """
    return "<h1>Hello, World!</h1>"


def start_rates_api() -> None:
    """ start rates api """
    app.run()

