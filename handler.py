import json

import os
from glm.generic_lambda_handler import lambda_handler as generic_lambda_handler

from flask_app import app
import xl_bot
import dungeon_gossiper


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
