import time
import json
import os
from lib.command_parser import execute_command
from lib.printer import Printer
from lib.irc_connector import connect_to_twitch
from lib.character import Character
from lib.morgue_parser import fetch_skills
from lib.morgue_db import MorgueDB


def handler(event, context):
    print("I'm twitch_chat_bot!")
    # print(f"event: {event}")
    # print(f"context: {context}")

    character = Character(character=None)
    server = connect_to_twitch()
    printer = Printer(server, disable_twitch=False, character=character)

    for record in event["Records"]:

        if "kinesis" in record:
            import base64

            data = record["kinesis"]["data"]
            base64_decoded = base64.b64decode(data)
            message = base64_decoded.decode("utf")

            print("=========================\n")
            print(message)
            print("=========================\n")

            message_info = json.loads(message)

            print("=========================\n")
            print(message_info)
            print("=========================\n")

            msg = message_info["message"]
            printer.send_msg(msg)
            time.sleep(1)
        else:
            print("=========================\n")
            print(record)
            print("=========================\n")


# handler({}, {})
