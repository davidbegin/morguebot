import json
import os

from flask import Flask

from glm.generic_lambda_handler import lambda_handler as generic_lambda_handler

app = Flask(__name__)



# I think a really basic twitch chat version of this would be super cool.
# But people need Oauth Token, but we could help!!!


@app.route("/echo/<thang>")
def echo(thang):
    return thang


@app.route("/upper/<thang>")
def upper(thang):
    return thang.upper


def async_handler(messages, context):
    print(messages)


def lambda_handler(event, context):
    result = generic_lambda_handler(
        event=event, context=context, flask_app=app, async_handler=async_handler
    )
    return result
