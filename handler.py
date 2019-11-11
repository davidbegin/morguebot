import os
from glm.generic_lambda_handler import lambda_handler as generic_lambda_handler


if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
    app = None
else:
    print("Hey we aren't a lambda!")
    app = None
    # from flask import Flask
    # app = Flask(__name__)


def async_handler(messages, context):
    print(messages)


def lambda_handler(event, context):
    return generic_lambda_handler(event, context, app, async_handler)
