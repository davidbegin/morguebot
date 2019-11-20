import json

import os
from glm.generic_lambda_handler import lambda_handler as generic_lambda_handler

from lib.command_executor import print_the_help
from lib.command_executor import Formatter
from lib.kinesis import send_chat_to_stream
from lib.morgue_saver import morgue_saver
from lib.character import Character

# ========================================================================================

from flask import Flask

app = Flask(__name__)


@app.route("/xl-bot/help")
def help():
    logger = None
    print_the_help(logger)
    return "We Helped!"


@app.route("/xl-bot/fetch/<name>")
def fetch(name):
    character = Character(name=name)
    morgue_saver(character, character.non_saved_morgue_file(), True)
    return f"Fetched {name}'s Morgue File!"


# Should we have it /name/command or /command/name
@app.route("/xl-bot/weapons/<name>")
def weapons(name):
    character = Character(name=name)
    formatter = Formatter(character)
    msg = formatter.print_weapons()
    if msg:
        send_chat_to_stream(msg)
        return " ".join(msg)
    else:
        return "No Weapons Found!"


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
