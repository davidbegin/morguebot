import json

import os
from glm.generic_lambda_handler import lambda_handler as generic_lambda_handler

# ========================================================================================

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/xl-bot/cool")
def cool():
    print("We did it! We were routed from /xl-bot/cool to this awesome method cool()")
    return "Woah"


# ========================================================================================


def async_handler(messages, context):
    print(messages)


def lambda_handler(event, context):
    result = generic_lambda_handler(
        event=event, context=context, flask_app=app, async_handler=async_handler
    )
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(f"{result}")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return result
