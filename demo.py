import json
import os

from flask import Flask

from generic_lambda_handler import generic_lambda_handler


app = Flask(__name__)


@app.route("/echo/<thang>")
def echo(thang):
    return thang


@app.route("/upper/<thang>")
def upper(thang):
    return thang.upper


def async_handler(messages, context):
    print(messages)


def lambda_handler(event, context):
    return generic_lambda_handler(
        event=event, context=context, flask_app=app, async_handler=async_handler
    )
