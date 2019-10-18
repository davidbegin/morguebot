import time
import base64
import json
import os

from lib.command_parser import execute_command
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB

from lib.irc_connector import connect_to_twitch


def send_msg(self, msg):
    # TODO: Make this configurable
    channel = "#beginbot"

    if not self.disable_twitch:
        if msg:
            result = self.server.send(
                bytes("PRIVMSG " + channel + " :" + msg + "\n", "utf-8")
            )


def process_kinesis_message(message):
    try:
        msg = json.loads(message)["Message"]
        if msg:
            print(f"msg {type(msg)}: {msg}")
            if type(msg) is list:
                for m in msg:
                    print(f"m: {m}")
                    printer.send_msg(m)
            else:
                printer.send_msg(msg)

        else:
            print("YO YOUR MESSAGE IS NONE")
    except Exception as e:
        print(e)


def process_kinesis_record(record):
    kinesis_record = record["kinesis"]
    data = kinesis_record["data"]
    base64_decoded = base64.b64decode(data)
    message = base64_decoded.decode("utf")

    if "Message" in message:
        process_kinesis_message(message)
    elif "default" in message:
        printer.send_msg(message["default"])
    else:
        printer.send_msg(json.dumps(message))


def send_twitch_message(event):
    server = connect_to_twitch()
    character = Character(character=None)

    for record in event["Records"]:
        process_kinesis_record(record)


def parse_json(item):
    try:
        return json.loads(item)
    except:
        return None
